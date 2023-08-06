# author: delta1037
# Date: 2022/01/08
# mail:geniusrabbit@qq.com
import copy

import NotionDump
from NotionDump.Dump.block import Block
from NotionDump.Dump.database import Database
from NotionDump.Dump.page import Page
from NotionDump.Notion.Notion import NotionQuery
from NotionDump.utils import internal_var, common_op


class Dump:
    def __init__(
            self,
            dump_id,
            query_handle: NotionQuery,
            export_child_pages=False,
            page_parser_type=NotionDump.PARSER_TYPE_MD,
            db_parser_type=NotionDump.PARSER_TYPE_PLAIN,
            dump_type=NotionDump.DUMP_TYPE_PAGE
    ):
        self.dump_id = dump_id.replace('-', '')
        self.query_handle = query_handle
        # 是否导出子页面
        self.export_child_page = export_child_pages
        self.page_parser_type = page_parser_type
        self.db_parser_type = db_parser_type
        self.dump_type = dump_type

        self.handle = None
        if dump_type == NotionDump.DUMP_TYPE_PAGE:
            self.handle = Page(
                page_id=self.dump_id,
                query_handle=self.query_handle,
                export_child_pages=self.export_child_page,
                page_parser_type=self.page_parser_type,
                db_parser_type=self.db_parser_type
            )
        elif dump_type == NotionDump.DUMP_TYPE_BLOCK:
            self.handle = Block(
                block_id=self.dump_id,
                query_handle=self.query_handle,
                export_child_pages=self.export_child_page,
                page_parser_type=self.page_parser_type,
                db_parser_type=self.db_parser_type
            )
        elif dump_type == NotionDump.DUMP_TYPE_DB_TABLE:
            self.handle = Database(
                database_id=self.dump_id,
                query_handle=self.query_handle,
                export_child_pages=self.export_child_page,
                page_parser_type=self.page_parser_type,
                db_parser_type=self.db_parser_type
            )
        else:
            common_op.debug_log("unknown dump type:" + str(self.dump_type), level=NotionDump.DUMP_MODE_DEFAULT)

    # show_child_page
    @staticmethod
    def __get_pages_detail():
        return internal_var.PAGE_DIC

    # 获取到所有的BLOCK数据
    def dump_to_file(self, file_name=None):
        if self.handle is None:
            common_op.debug_log("dump init fail", level=NotionDump.DUMP_MODE_DEFAULT)
            return ""
        # 递归时第一个block单独作为一个main page存放
        self.handle.dump_to_file(file_name=file_name)
        self.query_handle.safe_save()

        pages_detail = copy.deepcopy(internal_var.PAGE_DIC)
        internal_var.PAGE_DIC = {}
        return pages_detail

    def dump_to_db(self):
        if self.handle is None:
            common_op.debug_log("dump init fail", level=NotionDump.DUMP_MODE_DEFAULT)
            return ""
        # 将内容导出到数据库
        self.handle.dump_to_db()
        self.query_handle.safe_save()

        pages_detail = copy.deepcopy(internal_var.PAGE_DIC)
        internal_var.PAGE_DIC = {}
        return pages_detail

    # 源文件，直接输出成json; 辅助测试使用
    def dump_to_json(self, json_name=None):
        if self.handle is None:
            common_op.debug_log("dump init fail", level=NotionDump.DUMP_MODE_DEFAULT)
            return ""

        self.handle.dump_to_json(json_name=json_name)
        self.query_handle.safe_save()

        pages_detail = copy.deepcopy(internal_var.PAGE_DIC)
        internal_var.PAGE_DIC = {}
        return pages_detail
