import os
import xlrd
import numpy
import pyecharts
from xlutils.copy import copy


def getAllTargetCsv(path):
    all = os.listdir(path)
    return [os.path.join(path, item) for item in all if 'csv' in item]


def parseCsvs(src):
    # column CodechalDecode::Execute  CreateVideoDecoder_D3D11_1
    # column DxvaEncodeHEVC_Create  DxvaEncodeHEVC_Execute
    # raw Average (ms)
    filename = getName(src)
    chalName = ""
    chalAvg = ""
    videoName = ""
    videoAvg = ""
    dxvacName = ""
    dxvacAvg = ""
    dxvaeName = ""
    dxvaeAvg = ""
    content = readCsvFile(src)
    lines = content.split("\n")
    for line in lines:
        if "LD" in filename:
            if "CodechalDecode::Execute" in line:
                chals = line.strip().split(",")
                chalName = chals[0]
                chalAvg = chals[2]
            if "First Frame Time" in line:
                videos = line.strip().split(",")
                videoName = videos[0]
                videoAvg = videos[2]
        if "AV" in filename:
            if "decode::Av1PipelineG12::Execute1" in line:
                chals = line.strip().split(",")
                chalName = chals[0]
                chalAvg = chals[2]
            if "First Frame Time" in line:
                videos = line.strip().split(",")
                videoName = videos[0]
                videoAvg = videos[2]
        if "x0" in filename:
            if "First Frame Time" in line:
                dxvacs = line.strip().split(",")
                dxvacName = dxvacs[0]
                dxvacAvg = dxvacs[2]
            if "DxvaEncodeHEVC_Execute" in line:
                dxvaes = line.strip().split(",")
                dxvaeName = dxvaes[0]
                dxvaeAvg = dxvaes[2]
    return (filename, chalName, chalAvg, videoName, videoAvg, dxvacName, dxvacAvg, dxvaeName, dxvaeAvg)


def getName(src):
    return src.split("\\")[-1].split(".")[0]


def readCsvFile(src):
    content = ""
    with open(src, 'r') as fp:
        content = fp.read()
    return content


def getPath():
    dir_list = os.listdir()
    path = []
    del dir_list[0]
    del dir_list[0]
    for i in range(len(dir_list)):
        path.append(os.path.join(os.getcwd(), dir_list[i]))
    print(dir_list)
    return path, dir_list


# def getDayIndex(dirNum):
#     dayIndex = []
#     for i in range(dirNum):
#         day = f'day{i}'
#         exec('dayIndex.append(day)')
#     return dayIndex


def clearPath():
    delPathLog = os.path.join(os.getcwd(), 'debug.log')
    if os.path.exists(delPathLog):
        os.remove(delPathLog)
    delPathHtml = os.path.join(os.getcwd(), 'PerformanceDisplay.html')
    if os.path.exists(delPathHtml):
        os.remove(delPathHtml)


def xlsInit(oldbook):
    newWb = copy(oldbook)  # 复制
    newWs = newWb.get_sheet(0)  # 取sheet表
    for p in range(2, 120):
        for q in range(2):
            newWs.write(p, q, '')
    for p in range(2, 120):
        for q in range(4, 20):
            newWs.write(p, q, '')
    for q in range(4, 20):
            newWs.write(1, q, '')
    return newWs, newWb


def getMostCase(dirNum, path):
    caseNumArr1 = []
    caseNumArr2 = []
    for j in range(dirNum):
        currentPath = path[j]
        targets = getAllTargetCsv(currentPath)
        rawData = []
        for item in targets:
            rawData.append(parseCsvs(item))
        rawData = numpy.array(rawData)
        allCaseName = rawData[:, 0]  # 获取所有case名字

        caseNameAVLD = []
        caseNameX = []
        # 读取AV LD name/value
        for item in allCaseName:
            if 'AV' in item or 'LD' in item:
                caseNameAVLD.append(item)
            else:
                caseNameX.append(item)
        caseNumArr1.append(len(caseNameAVLD))
        caseNumArr2.append(len(caseNameX))
    caseDecoderDay = caseNumArr1.index(max(caseNumArr1, key=abs))
    caseNum1 = max(caseNumArr1)
    caseEncoderDay = caseNumArr2.index(max(caseNumArr2, key=abs))
    caseNum2 = max(caseNumArr2)
    return caseDecoderDay, caseEncoderDay, caseNum1, caseNum2


def getDataXls(dirNum, newWs, newWb, dayIndex, path, caseDecoderDay, caseEncoderDay, caseNum1, caseNum2):
    currentPath = path[caseDecoderDay]
    targets = getAllTargetCsv(currentPath)
    rawData = []
    for item in targets:
        rawData.append(parseCsvs(item))
    allDecodeCaseName = [x[0] for x in rawData]  # 获取所有decode case名字

    currentPath = path[caseEncoderDay]
    targets = getAllTargetCsv(currentPath)
    rawData = []
    for item in targets:
        rawData.append(parseCsvs(item))
    allEncodeCaseName = [x[0] for x in rawData]  # 获取所有encode case名字
    allCaseName = allDecodeCaseName + allEncodeCaseName
    allCaseName = list(set(allCaseName))
    allCaseName = sorted(allCaseName)

    for i in range(caseNum1):
        newWs.write(2 * i + 2, 0, allCaseName[i])  # AV LD casename写入表格第一列
        newWs.write(2 * i + 2, 1, 'CodechalDecode::Execute')  # AV LD CodechalDecode::Execute写入表格第二列
        newWs.write(2 * i + 3, 1, 'First Frame Time')  # AV LD CreateVideoDecoder_D3D11_1写入表格第二列
    for i in range(3):
        newWs.write(2 * i + 2, 0, allCaseName[i])  # AV LD casename写入表格第一列
        newWs.write(2 * i + 2, 1, 'decode::Av1PipelineG12::Execute1')  # AV LD CodechalDecode::Execute写入表格第二列
        newWs.write(2 * i + 3, 1, 'First Frame Time')  # AV LD CreateVideoDecoder_D3D11_1写入表格第二列
    for j in range(caseNum2):
        newWs.write(2 * j + 2 * caseNum1 + 2, 0, allCaseName[j + caseNum1])  # x0 casename写入表格内LD下面 第一列
        newWs.write(2 * j + 2 * caseNum1 + 2, 1, 'First Frame Time')  # x0 DxvaEncodeHEVC_Create写入表格内LD下面 第二列
        newWs.write(2 * j + 2 * caseNum1 + 3, 1, 'DxvaEncodeHEVC_Execute')  # x0 DxvaEncodeHEVC_Execute写入表格内LD下面 第二列

    for k in range(dirNum):
        currentPath = path[k]
        targets = getAllTargetCsv(currentPath)
        rawData = []
        for item in targets:
            rawData.append(parseCsvs(item))
        rawData = numpy.array(rawData)
        allRealCaseName = rawData[:, 0]  # 获取所有case名字
        caseNameAVLD = []
        caseNameX = []
        # 读取AV LD name/value
        for item in allRealCaseName:
            if 'AV' in item or 'LD' in item:
                caseNameAVLD.append(item)
            else:
                caseNameX.append(item)
        caseRealNum1 = len(caseNameAVLD)
        caseRealNum2 = len(caseNameX)

        # 读取Decode name/value
        caseValueExe = []
        caseValueDec = []
        for m in range(caseRealNum1):
            caseValueExe.append(rawData[m, 2])
            caseValueDec.append(rawData[m, 4])
        # print("caseValueExe = ", caseValueExe)
        # print("caseValueDec = ", caseValueDec)
        # print("k, caseRealNum1, caseRealNum2 = ", k, caseRealNum1, caseRealNum2)
        # print("rawData = ", rawData)

        # 读取Encode name/value
        caseValueXC = []
        caseValueXE = []
        for n in range(caseRealNum1, caseRealNum1 + caseRealNum2):
            caseValueXC.append(rawData[n, 6])
            caseValueXE.append(rawData[n, 8])
        # print("caseValueXC = ", caseValueXC)
        # print("caseValueXE = ", caseValueXE)
        newWs.write(1, k + 4, dayIndex[k])
        for o in range(0, caseRealNum1):
            newWs.write(2 * o + 2, k + 4, caseValueExe[o])  # AV LD CodechalDecode::Execute写入表格第五列-
            newWs.write(2 * o + 3, k + 4, caseValueDec[o])  # AV LD CreateVideoDecoder_D3D11_1写入表格第五列-
        for p in range(0, caseRealNum2):
            newWs.write(2 * p + 2 * caseNum1 + 2, k + 4, caseValueXC[p])  # x0 DxvaEncodeHEVC_Create写入表格内LD下面 第五列-
            newWs.write(2 * p + 2 * caseNum1 + 3, k + 4, caseValueXE[p])  # x0 DxvaEncodeHEVC_Execute写入表格内LD下面 第五列
    newWb.save("NH.xls")  # 保存至result路径
    caseNum = 2 * (caseNum1 + caseNum2) + 2
    return caseNum


def xlsDisplay(caseNum, dirNum):
    data = xlrd.open_workbook(r'NH.xls')
    st = data.sheet_by_index(0)
    page = pyecharts.Page()
    case_name = [str(st.cell_value(i, 0)) for i in range(2, caseNum)]

    x1 = [str(st.cell_value(1, i)) for i in range(4, 4 + dirNum)]
    dataName = [str(st.cell_value(i, 1)) for i in range(2, caseNum)]

    for j in range(2, caseNum):
        y1 = [str(st.cell_value(j, i)) for i in range(4, 4 + dirNum)]
        y2 = [str(st.cell_value(j, 2)) for i in range(4, 4 + dirNum)]
        # y3 = [str(st.cell_value(j, 3)) for i in range(4, 4 + dirNum)]
        if case_name[j - 2] == '':
            line1 = pyecharts.Line(case_name[j - 3] + "-" + dataName[j - 2], "Performance Comparison ：", title_text_size=13, width=1000)
            line1.add("DG2 Performance", x1, y1, line_width=4, label_pos='bottom', is_label_show=True,
                      is_datazoom_show=False,
                      mark_point=["max", "min"], mark_point_symbolsize=70, is_stack=True)  # 标题
            line1.add("TGL-NH", x1, y2, line_width=3, is_label_show=False, label_pos='bottom', is_datazoom_show=False,
                      line_type='dotted')
            # line1.add("MTL-NH", x1, y3, line_width=3, is_datazoom_show=False, label_pos='bottom', is_label_show=False,
            # line_type='dotted', line_color='green')
            page.add(line1)
        else:
            line2 = pyecharts.Line(case_name[j - 2] + "-" + dataName[j - 2], "Performance Comparison ：", title_text_size=13, width=1000)
            line2.add("DG2 Performance", x1, y1, line_width=4, label_pos='bottom', is_label_show=True,
                      is_datazoom_show=False,
                      mark_point=["max", "min"], mark_point_symbolsize=70, is_stack=True)  # 标题
            line2.add("TGL-NH", x1, y2, line_width=3, is_label_show=False, label_pos='bottom', is_datazoom_show=False,
                      line_type='dotted')
            # line2.add("MTL-NH", x1, y3, line_width=3, is_datazoom_show=False, label_pos='bottom', is_label_show=False,
            # line_type='dotted', line_color='green')
            page.add(line2)
    page.render(r"PerformanceDisplay.html")


def main():
    clearPath()
    path, dayIndex = getPath()
    dirNum = len(path)
    caseDecoderDay, caseEncoderDay, caseNum1, caseNum2 = getMostCase(dirNum, path)
    print("caseDecoderDay, caseEncoderDay = ", caseDecoderDay, caseEncoderDay)
    print("caseNum1, caseNum2 = ", caseNum1, caseNum2)
    # dayIndex = getDayIndex(dirNum)
    oldbook = xlrd.open_workbook('NH.xls', formatting_info=True)
    newWs, newWb = xlsInit(oldbook)
    caseNum = getDataXls(dirNum, newWs, newWb, dayIndex, path, caseDecoderDay, caseEncoderDay, caseNum1, caseNum2)
    xlsDisplay(caseNum, dirNum) # 可视化


if __name__ == "__main__":
    main()