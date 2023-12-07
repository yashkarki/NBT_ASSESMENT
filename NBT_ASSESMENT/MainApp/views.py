from django.shortcuts import render
from .forms import IntervalForm
from django.http import HttpResponse
import pandas as pd
import asyncio
import json

# Create your views here.
def convert_timeframe(interval):
    df = pd.read_csv("MainApp/static/demofile.csv",
                     parse_dates=[['DATE', 'TIME']])
    # print(df, "fjkdkjfdkj")
    df_new = df[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE_TIME']]
    df_new.rename(str.lower,axis='columns')
    # df_new.rename(columns={'OPEN': 'open', 'HIGH': 'high', 'LOW': 'low', 'CLOSE': 'close', 'DATE_TIME':'date'})
    # print("dgg",df_new,interval,"hhjhj")
    candle_list = df_new.values.tolist()
    final_list=[]
    for i in range(0,len(candle_list),int(interval)):
        final_list.append(candle_list[i])

    return final_list

async def handle_uploaded_file(f,interval):
    with open('MainApp/static/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # df = pd.read_csv("MainApp/static/"+f.name)

    # df = pd.read_csv("MainApp/static/demofile.csv",parse_dates=[['DATE','TIME']])
    # print(df,"fjkdkjfdkj")
    # df_new=df[['OPEN','HIGH','LOW','CLOSE','DATE_TIME']]
    candle_list= convert_timeframe(interval)
    # print(candle_list,"--------")
    for item in candle_list:
        item[-1] = item[-1].isoformat()
    # json_data = json.dumps(candle_list)
    # print(json_data,"fklglkfgkljhfkl")
    with open('outputfile', 'w') as fout:
        json.dump(candle_list,fout)
    # print(json_data)


   

    
    # print(df.head(50),"---head")
    # for i,row in df.iloc[:101].iterrows():
    #     print(row,"----------")
    #     candle_list.append(row)

    # print(candle_list,"-------")


def IndexPage(request):
    # print("request.post-----",request.method )
    if request.method == 'POST':
        interval_form = IntervalForm(request.POST, request.FILES)
        if interval_form.is_valid():
            interval = request.POST.get('interval')
            # print(request.POST.get('interval'),"dlfldkf")
            asyncio.run(handle_uploaded_file(request.FILES['file'],interval))

            return render(request, "response.html")
    else:
        intervals = IntervalForm()
        return render(request, "index.html", {'form': intervals})

# def ConvertIntoInterval(request):
#     print("request.post-----")
#     if request.method == 'POST':
#         interval_form = IntervalForm(request.POST, request.FILES)
#         if interval_form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponse("File uploaded successfuly")
#     else:
#         intervals = IntervalForm()
#         return render(request, "index.html", {'form': intervals})
