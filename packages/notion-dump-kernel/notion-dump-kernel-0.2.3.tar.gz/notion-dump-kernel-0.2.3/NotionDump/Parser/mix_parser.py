# author: delta1037
# Date: 2022/01/10
# mail:geniusrabbit@qq.com
import copy
import os

import NotionDump
from NotionDump.Notion.Notion import NotionQuery
from NotionDump.Parser.block_parser import BlockParser
from NotionDump.Parser.database_parser import DatabaseParser
from NotionDump.utils import common_op, internal_var


# 混合递归调用，主要是为Page和Database类型
class MixParser:
    # 初始化
    def __init__(
            self,
            mix_id,
            query_handle: NotionQuery,
            export_child_pages=False,
            page_parser_type=NotionDump.PARSER_TYPE_MD,
            db_parser_type=NotionDump.PARSER_TYPE_PLAIN,
            col_name_list=None,  # 数据库使用的字段
    ):
        self.mix_id = mix_id
        self.query_handle = query_handle
        self.page_parser_type = page_parser_type
        self.db_parser_type = db_parser_type

        # 是否导出子页面,也就是递归操作
        self.export_child_page = export_child_pages

        # 创建临时文件夹
        self.tmp_dir = NotionDump.TMP_DIR
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)

        # 解析器
        # 这里传入handle是为了子块的解析
        self.block_parser = BlockParser(
            block_id=self.mix_id,
            query_handle=self.query_handle,
            parser_type=self.page_parser_type,
            export_child_pages=self.export_child_page
        )
        # 初始化一个Database对象，这里page id无关紧要
        self.database_parser = DatabaseParser(
            self.mix_id,
            parser_type=self.db_parser_type,
            export_child_pages=self.export_child_page
        )

        # 收集解析中发证的错误
        self.error_list = []

    # 调试时显示子页面内容
    def __test_show_child_page(self):
        if NotionDump.DUMP_MODE == NotionDump.DUMP_MODE_DEBUG:
            print("in page_id: ", self.mix_id, internal_var.PAGE_DIC)

    def __recursion_mix_parser(self, is_main=False, col_name_list=None):
        root_name = None
        update_flag = False
        recursion_page = copy.deepcopy(internal_var.PAGE_DIC)
        for child_id in recursion_page:
            # 判断页面是子页面还是链接页面，链接页面不进行解析(因为添加链接页面时把原页面也加进来了)
            if common_op.is_link_page(child_id, recursion_page[child_id]):
                common_op.update_page_recursion(child_id, recursion=True)
                continue
            # 判断页面是否已经操作过
            if not common_op.is_page_recursion(child_id):
                continue

            update_flag = True
            common_op.debug_log("start child_page_id=" + child_id)
            self.__test_show_child_page()
            # 先更新页面的状态，无论获取成功或者失败都过去了，只获取一次
            common_op.update_page_recursion(child_id, recursion=True)
            common_op.debug_log("S process id " + child_id, level=NotionDump.DUMP_MODE_DEFAULT)
            page_title = None
            tmp_filename = None
            if common_op.is_page(child_id):
                # 页面信息
                page_detail = self.query_handle.retrieve_page(child_id)
                # 页面内容
                page_json = self.query_handle.retrieve_block_children(child_id)
                if page_json is None or page_detail is None:
                    common_op.debug_log("get page error, id=" + child_id, level=NotionDump.DUMP_MODE_DEFAULT)
                    self.error_list.append("get page error, id=" + child_id)
                    continue
                # 解析属性文本到变量中
                page_properties = None
                if NotionDump.S_PAGE_PROPERTIES or common_op.is_page_soft(child_id):
                    # 获取文本
                    page_properties, page_title = self.database_parser.database_to_md(page_detail, new_id=child_id)
                # 解析内容到临时文件中
                tmp_filename = self.block_parser.block_to_md(page_json, page_detail=page_properties, new_id=child_id)
                # 处理遇到的子页面
                child_pages_dic = self.block_parser.get_child_pages_dic()
                if NotionDump.S_PAGE_PROPERTIES:
                    db_child_pages_dic = self.database_parser.get_child_pages_dic()
                    for db_child_dic_key in db_child_pages_dic:
                        if db_child_dic_key not in child_pages_dic:
                            child_pages_dic[db_child_dic_key] = db_child_pages_dic[db_child_dic_key]
            elif common_op.is_db(child_id):
                db_info = self.query_handle.retrieve_database(child_id)
                # page里面搞一个Database的解析器
                db_detail = self.query_handle.query_database(child_id)

                if db_detail is None:
                    # db_info不是必须的，但是在link数据库获取不到
                    common_op.debug_log("get database error, id=" + child_id, level=NotionDump.DUMP_MODE_DEFAULT)
                    self.error_list.append("get database error, id=" + child_id)
                    continue
                # 获取解析后的数据
                tmp_filename = self.database_parser.database_to_file(db_detail, new_id=child_id, col_name_list=col_name_list)
                child_pages_dic = self.database_parser.get_child_pages_dic()
            elif common_op.is_download(child_id):
                # 可下载类型
                # 获取下载后的数据
                tmp_filename = self.query_handle.download_to_file(download_id=child_id, child_page_item=recursion_page[child_id])
                child_pages_dic = {}
                # 尝试下载，没下载成功
                if tmp_filename == "" and not NotionDump.FILE_WITH_LINK:
                    common_op.debug_log("file download error, id=" + child_id, level=NotionDump.DUMP_MODE_DEFAULT)
                    self.error_list.append("download error, link:" + recursion_page[child_id]["link_src"])
                    continue
            else:
                common_op.debug_log("!!! unknown child id type, id=" + child_id, level=NotionDump.DUMP_MODE_DEFAULT)
                self.error_list.append("!!! unknown child id type, id=" + child_id)
                continue

            common_op.debug_log("E process id " + child_id + " success", level=NotionDump.DUMP_MODE_DEFAULT)
            # 再更新本地的存放路径
            common_op.update_child_page_stats(child_id, dumped=True, main_page=is_main, local_path=tmp_filename, page_title=page_title)
            if is_main:
                root_name = tmp_filename
            # 从页面里获取到所有的子页面,并将子页面添加到父id中
            common_op.update_child_pages(child_pages_dic, child_id)

            # 调试
            common_op.debug_log("# end child_page_id=", child_id)
            self.__test_show_child_page()

        if update_flag:
            self.__recursion_mix_parser()
        return root_name

    def mix_parser(self, root_id, id_type, col_name_list=None):
        # col_name_list 是数据库的可选字段
        common_op.update_child_page_stats(root_id, main_page=True, page_type=id_type)
        root_filename = self.__recursion_mix_parser(True, col_name_list)
        internal_var.PAGE_DIC["errors"] = self.error_list
        return root_filename

    def database_collection(self, json_handle, json_type, col_name_list=None):
        # 只能获取数据库类型
        common_op.debug_log("parser_type:" + json_type, level=NotionDump.DUMP_MODE_DEFAULT)
        if json_type == "database":
            return self.database_parser.database_to_dic(json_handle, col_name_list=col_name_list)
        elif json_type == "block":
            common_op.debug_log("need database get type:" + json_type, level=NotionDump.DUMP_MODE_DEFAULT)
            return None
        else:
            common_op.debug_log("unknown parser_type:" + json_type, level=NotionDump.DUMP_MODE_DEFAULT)
            return None
