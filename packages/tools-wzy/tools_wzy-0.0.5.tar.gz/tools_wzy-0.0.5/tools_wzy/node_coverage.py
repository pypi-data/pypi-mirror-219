import pandas as pd
import json
from datetime import datetime, timedelta


def coverage_to_excel(data_path='./2023-06-29~2023-07-02CCTV数据源-绕机作业数据 (5).xls', out_floder='.',
                      out_name='节点覆盖率统计.xlsx', txt_path='节点较多的机位列表20230714.txt'):
    # txt_path 参与统计的机位

    out_path = out_floder + '/' + out_name
    try:
        df = pd.read_excel(data_path, sheet_name='Worksheet')
    except:
        df = pd.read_excel(data_path, sheet_name='Sheet1')
    # 按照机位进行升序排列
    df = df.sort_values(by='机位')
    # 获取到列名
    cols = df.columns

    # 更换列名
    with open("tools_wzy/node_name_excel.json", "r", encoding="utf-8") as f:
        node_excel = json.load(f)
    with open("tools_wzy/node_name.json", "r", encoding="utf-8") as f:
        node_names = json.load(f)
    node_key = {v: k for k, v in node_names.items()}
    temp = list(cols)[6::2]
    for nodei in temp:
        # print(node_key[node_excel[nodei]])
        df.rename(columns={nodei: node_key[node_excel[nodei]]}, inplace=True)
        df.rename(columns={nodei + '-更新时间': node_key[node_excel[nodei]] + '_up'}, inplace=True)
    df.rename(columns={'机位': 'stand_id'}, inplace=True)
    df.rename(columns={'服务类型': 'service_type'}, inplace=True)

    STA_NODE = ['ATPT', 'CTBT', 'ATCO', 'ATDO', 'ABTT', 'AIBT', 'ARLS']
    STD_NODE = ['ABLT', 'ATCC', 'AOBT', 'LTPT', 'PCST', 'PCET', 'JYET', 'JYST', 'LTBT', 'ATTT', 'ATDC', 'LSW']
    all_node = STA_NODE + STD_NODE

    excel_writer = pd.ExcelWriter(out_path)
    # 节点名称对应
    temp = list(
        zip(list(node_excel.keys()), list(node_excel.values()), [node_key[i] for i in list(node_excel.values())]))
    temp = pd.DataFrame(temp, columns=['excel中节点名称', '数据库中节点名称', '数据库中节点代码'])
    temp.to_excel(excel_writer, sheet_name='节点名称对应', index=False, engine='openpyxl')

    with open(txt_path, 'r') as file:
        aprons = [int(line.strip()) for line in file]
    df_apron_need = pd.DataFrame(aprons, columns=['设置以下机位参与覆盖率统计'])
    df_apron_all = pd.DataFrame(
        df.loc[:, 'stand_id'].drop_duplicates().reset_index(drop=True).rename('以下实际覆盖机位'))
    df_apron_need = pd.DataFrame(
        pd.merge(df_apron_all, df_apron_need, left_on='以下实际覆盖机位', right_on='设置以下机位参与覆盖率统计')[
            '设置以下机位参与覆盖率统计'])
    df_apron_combine = pd.concat([df_apron_all, df_apron_need], axis=1)
    df_apron_combine.to_excel(excel_writer, sheet_name='机位覆盖情况', index=False, engine='openpyxl')
    # 删除不参与统计的
    aprons_noneed = df_apron_all[
                        ~df_apron_all['以下实际覆盖机位'].isin(df_apron_need['设置以下机位参与覆盖率统计'])].iloc[:,
                    0].tolist()
    df = df.drop(index=df[df['stand_id'].isin(aprons_noneed)].index)

    df.to_excel(excel_writer, sheet_name='参与统计的机位信息', index=False, engine='openpyxl')

    # STA_NODE，进港
    df_node_fa = df.loc[df['进出港'] == '进港', ['fid', 'stand_id', 'service_type'] + STA_NODE]
    df_node_fa.replace('--', 0, inplace=True)
    df_node_fa.replace('20\d\d-\d\d-\d\d \d\d:\d\d:\d\d', 1, regex=True, inplace=True)
    # 货运航班不统计廊桥、客梯车
    df_node_fa.loc[~df_node_fa['service_type'].isin(['W/Z', 'Z/P', 'L/W', 'Z/X', 'C/B']), 'ARLS'] = pd.NA  # 客梯车到达
    df_node_fa.loc[~df_node_fa['service_type'].isin(['W/Z', 'Z/P', 'L/W', 'Z/X', 'C/B']), 'CTBT'] = pd.NA  # 廊桥靠近
    df_node_fa.loc[df_node_fa['stand_id'] > 200, 'CTBT'] = pd.NA  # 远机位不统计廊桥
    df_node_fa.loc[df_node_fa['stand_id'] <= 200, 'ARLS'] = pd.NA  # 近机位不统计客梯车
    df_coverage_a = df_node_fa.groupby('stand_id')[STA_NODE].mean()
    # df_coverage_a.loc[df_coverage_a.index > 200, 'CTBT'] = pd.NA
    # df_coverage_a.loc[df_coverage_a.index <= 200, 'ARLS'] = pd.NA
    df_coverage_all_a = df_node_fa[STA_NODE].mean()

    # STD_NODE，出港
    df_node_fd = df.loc[df['进出港'] == '出港', ['fid', 'stand_id', 'service_type'] + STD_NODE]
    df_node_fd.replace('--', 0, inplace=True)
    df_node_fd.replace('20\d\d-\d\d-\d\d \d\d:\d\d:\d\d', 1, regex=True, inplace=True)
    # 货运航班不统计廊桥、客梯车、配餐
    df_node_fd.loc[~df_node_fd['service_type'].isin(['W/Z', 'Z/P', 'L/W', 'Z/X', 'C/B']), 'LSW'] = pd.NA
    df_node_fd.loc[~df_node_fd['service_type'].isin(['W/Z', 'Z/P', 'L/W', 'Z/X', 'C/B']), 'LTBT'] = pd.NA
    df_node_fd.loc[~df_node_fd['service_type'].isin(['W/Z', 'Z/P', 'L/W', 'Z/X', 'C/B']), 'PCST'] = pd.NA
    df_node_fd.loc[~df_node_fd['service_type'].isin(['W/Z', 'Z/P', 'L/W', 'Z/X', 'C/B']), 'PCET'] = pd.NA
    df_node_fd.loc[df_node_fd['stand_id'] > 200, 'LTBT'] = pd.NA  # 远机位不统计廊桥
    df_node_fd.loc[df_node_fd['stand_id'] <= 200, 'LSW'] = pd.NA  # 近机位不统计客梯车
    df_coverage_d = df_node_fd.groupby('stand_id')[STD_NODE].mean()
    # df_coverage_a.loc[df_coverage_a.index > 200, 'CTBT'] = pd.NA
    # df_coverage_a.loc[df_coverage_a.index <= 200, 'ARLS'] = pd.NA
    df_coverage_all_d = df_node_fd[STD_NODE].mean()

    # 合并、保存
    df_node_coverage = pd.concat([df_coverage_a, df_coverage_d], axis=1)
    col_name = [node_names[x] for x in all_node]
    df_node_coverage.columns = col_name
    df_node_coverage.to_excel(excel_writer, sheet_name='按照机位统计覆盖率', index=True, engine='openpyxl')

    # 保存
    s_node_coverage_all = pd.concat([df_coverage_all_a, df_coverage_all_d], axis=0)
    df_node_coverage_all = s_node_coverage_all.to_frame().T
    col_name = [node_names[x] for x in all_node]
    df_node_coverage_all.columns = col_name
    df_node_coverage_all.to_excel(excel_writer, sheet_name='整体覆盖率', index=False, engine='openpyxl')

    excel_writer._save()
    print("覆盖率统计文件：" + out_path)
    return out_path


def request_single_data_xls(request_date='2023-06-29', save_folder="../node_coverage_excels"):
    import requests
    save_name = request_date + 'CCTV数据源-绕机作业数据.xls'  # 没有直接从响应中读文件名，乱码没解决
    req_params = {'fdate': request_date}
    headers = {
        "Accept-Encoding": "gzip",
        "Cookie": "ci_session_pvg_acdm=290bcea98ce442dc094b844f691ff7daf033de31; goms_pvg_user_auth=kMFLe%2BrS7BEFHSHktVMN6RbfGZS2CI4tG0kWruXDbrA3vMTQxS0q3kEqNNmCIN500m04s6bRdEgMmvApRWeVrcu7xvetAuTv8Nx3tqcfgOOzOQR4DDztgkMdJExWvlg2F13GNR1sclDUvPJaMoy7R%2B97Bzx6d5oYgaorhZfcx1iL5igQEtndzMTLeRVfcvFeV4dfFlKp6oj2xXKvwh1B%2BNU3uOMihn89pA480dFR%2BjAR3eKQMbegMDwRiWOyCYEkLQx9AxCGx01eaqpzJkFnlm0ngS6g095uhcnbOrFcotc%3D; goms_pvg_user_default_airport=PVG",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }

    response = requests.get("https://pvg.goms.com.cn/flight/export_data/download_data_of_tongji_raojizuoye?",
                            params=req_params, headers=headers)

    print("request_date: " + request_date)
    print("url: " + response.url)
    print("status_code: " + str(response.status_code))  # 响应码
    if response.status_code == 200:
        save_path = save_folder + '/' + save_name
        with open(save_path, 'wb') as f:  # 将文件保存到本地
            f.write(response.content)
            print("文件已保存: " + save_path)
    return save_path


def request_data_xls(start_date, end_date, save_folder="../node_coverage_excels"):
    xls_path_list = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        xls_path = request_single_data_xls(date_str, save_folder)
        xls_path_list.append(xls_path)
        current_date += timedelta(days=1)
    return xls_path_list


def merge_xls(xls_path_list, save_folder, save_name='merged_file.xlsx'):
    save_path = save_folder + '/' + save_name
    merged_data = pd.DataFrame()
    for xls_path in xls_path_list:
        print("合并 -- " + xls_path)
        df = pd.read_excel(xls_path, engine='xlrd')
        merged_data = pd.concat([merged_data, df], ignore_index=True)
    merged_data.to_excel(save_path, engine='openpyxl', index=False)
    print("合并后文件：" + save_path)
    return save_path


def all(start_date, end_date, save_folder, out_name, txt_path):
    # 下载文件
    xls_path_list = request_data_xls(start_date, end_date, save_folder)
    print('-' * 80)
    # 合并文件
    merged_file = merge_xls(xls_path_list, save_folder, 'merged_file.xlsx')
    print('-' * 80)
    # 进行覆盖率统计
    coverage_to_excel(merged_file, save_folder, out_name, txt_path)
    print('-' * 80)


if __name__ == '__main__':
    # 可以使用all()一个函数完成，下面是一个案例，也可以按照all()的结构一步步写
    start_date = datetime(2023, 7, 12)
    end_date = datetime(2023, 7, 14)
    save_folder = r"D:\Zhiyuan\node_coverage_excels"
    out_name = "节点覆盖率统计.xlsx"
    txt_path = r"D:\Zhiyuan\files/节点较多的机位列表20230714.txt"
    all(start_date, end_date, save_folder, out_name, txt_path)
