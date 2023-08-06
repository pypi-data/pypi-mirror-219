
def main():
    from .screen_for_magPro import check_and_reform, modify_magPro_name_inGenbank
    from .get_parser import get_parser

    psi_res_path = get_parser().PsiResultPath
    csv_file_path = check_and_reform(psi_res_path)
    gbk_files_folder = get_parser().GenbankFilesPath
    if gbk_files_folder:
        modify_magPro_name_inGenbank(csv_file_path, gbk_files_folder)

#############################################
if __name__ == '__main__':
    main()