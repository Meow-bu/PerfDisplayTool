import os
import xlwt

def getAllTargetCsv(path):
   all = os.listdir(path)
   return [os.path.join(os.getcwd(),item) for item in all if 'csv' in item]


def parseCsvs(src):
   # column CodechalDecode::Execute  First Frame Time
   # column DxvaEncodeHEVC_Create  DxvaEncodeHEVC_Execute
   # raw Average (ms)
   filename=getName(src)
   chalName = ""
   chalAvg = ""
   videoName = ""
   videoAvg = ""
   dxvacName = ""
   dxvacAvg = ""
   dxvaeName=""
   dxvaeAvg=""
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
   return (filename,chalName,chalAvg,videoName,videoAvg,dxvacName,dxvacAvg,dxvaeName,dxvaeAvg)

def getName(src):
   return src.split("\\")[-1].split(".")[0]

def readCsvFile(src):
   content = ""
   with open(src,'r') as fp:
      content = fp.read()
   return content	  
   

   
def main():
   print("start to run...")
   currentPath = os.getcwd()
   targets = getAllTargetCsv(currentPath)
   rawData=[]
   for item in targets:
      rawData.append(parseCsvs(item))
   workbook = xlwt.Workbook(encoding="utf-8")
   worksheet = workbook.add_sheet("test")
   for i in range(len(rawData)):
      rd = rawData[i]
      worksheet.write(i,0,i+1)
      worksheet.write(i,1,rd[0])
      worksheet.write(i,2,rd[1])
      worksheet.write(i,3,rd[2])
      worksheet.write(i,4,rd[3])
      worksheet.write(i,5,rd[4])
      worksheet.write(i,6,rd[5])
      worksheet.write(i,7,rd[6])
      worksheet.write(i,8,rd[7])
      worksheet.write(i,9,rd[8])
   workbook.save("result.xls") 	  
   
   
if __name__ == "__main__":
   main()   