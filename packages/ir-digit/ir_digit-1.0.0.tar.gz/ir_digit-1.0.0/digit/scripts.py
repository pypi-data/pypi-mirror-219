import argparse
from .core import Core

def main():
    parser = argparse.ArgumentParser(prog="digit")
    subparsers = parser.add_subparsers(dest='command')

    parser.add_argument("-u", "--update-api-token", help="设置/更新个人的API-token")
    parser.add_argument("-c", "--category", help="查看分类体系中的编码与含义", default=None)
    parser.add_argument("-d","--delete", help="根据 data_id or name 删除个人资源")


    query_parser = subparsers.add_parser('query', help='子命令：查看平台现有资源')
    query_parser.add_argument("-t", "--type", help="指定资源类型查看，可选:data/card/useraccount/websetting/dataid", default='data')
    query_parser.add_argument("-i", "--id", help="选择特定id的资源查看", default=None)
    query_parser.add_argument("-d", "--detail", help="是否查看详情，默认为否", default=False)

    download_parser = subparsers.add_parser('download', help='子命令：下载资源到本地')
    download_parser.add_argument("-i", "--id-or-name", help="根据data_id_or_name下载对应的资源至本地，默认如果已经存在则不更新资源")
    download_parser.add_argument("-u", "--update", help="更新下载的资源")

    upload_parser = subparsers.add_parser('upload',help="子命令：上传资源")
    upload_parser.add_argument("-m" "--markdown-path",help="上传的markdown文件路径")
    upload_parser.add_argument("-c","--config-path",help="上传的config.json文件路径")

    run_parser = subparsers.add_parser('run', help='子命令：下载 + 加载 + 运行资源')
    run_parser.add_argument("-i", "--id-or-name", help="根据data_id_or_name下载对应的资源至本地，默认如果已经存在则不更新资源")
    run_parser.add_argument("-u", "--update", help="是否更新下载的资源",default=False)
    run_parser.add_argument("-ip","--imp_class", help="导入类的类型名称",default="DigitData")

    args = parser.parse_args()
    core = Core()

    if args.command == "query":
        core.get_resources(api_type=args.type, id=args.id, detail=args.detail)
    elif args.command == "download":
        core.download_repo(data_id_or_name=args.id_or_name, update=args.update)
    elif args.command =="upload":
        core.upload(md_instruction_path=args.markdown_path, config_path=args.config_path)
    elif args.command == "run":
        core.all_in_one(data_id_or_name=args.id_or_name, update=args.update, imp_class=args.imp_class)
    else:
        if args.update_api_token:
            core.update_api_token(new_token=args.update_api_token)
        elif args.category:
            core.get_category()
        elif args.delete:
            core.delete(data_id_or_name=args.delete)

        else:
            print("参数错误或未输入参数：")
            parser.print_help()


if __name__ == '__main__':
    main()
