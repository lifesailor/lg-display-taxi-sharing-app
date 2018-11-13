from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.http import require_POST

import json
import datetime
from itertools import cycle

from .models import Schedule, Reserve

# Create your views here.
@login_required(login_url='/accounts/signup/')
def schedule_list(request):
    
    #오늘 날짜 = date 오늘 요일 = day
    date = datetime.date.today()
    
    #일요일:0 , 월요일: 1, 화요일: 2, 수요일: 3, 목요일: 4, 금요일: 5, 토요일: 6
    dayNumber = (date.weekday()+1)%7
    weekday = ['일요일','월요일','화요일','수요일','목요일','금요일','토요일']
    
    for idx, val in enumerate(weekday):
        if idx == dayNumber:
            day = weekday[idx]
    
    holiday = holidayCheck(date.strftime('%m %d'))

    #휴일 여부 체크
    if holiday is True:
        subwaySchedule = Schedule.objects.filter(day=7, transport=0)
        busSchedule = Schedule.objects.filter(day=7, transport=1)
     
    else:
        #오늘 월롱역 지하철 시간표
        subwaySchedule = Schedule.objects.filter(day=dayNumber, transport=0)

        #오늘 월롱역 순환 버스 시간표
        rotateBusSchedule = Schedule.objects.filter(day=dayNumber, transport=1)
        
        #오늘 월롱역 복귀 버스 시간표
        returnBusSchedule = Schedule.objects.filter(day=dayNumber, transport=2)

    #오픈채팅방
    chatRoom = [
        'https://open.kakao.com/o/gVdrbGA', #1
        'https://open.kakao.com/o/gv9xbGA', #2
        'https://open.kakao.com/o/gjjCDCA', #3
        'https://open.kakao.com/o/gAX1aGA', #4
        'https://open.kakao.com/o/gEJOMQA', #5
        'https://open.kakao.com/o/gxg8MQA', #6
        'https://open.kakao.com/o/gK9BQQA', #7
        'https://open.kakao.com/o/gz5DQQA', #8
        'https://open.kakao.com/o/gc1HQQA', #9
        'https://open.kakao.com/o/gPWJQQA', #10
        'https://open.kakao.com/o/gAdaTdB', #11
        'https://open.kakao.com/o/g31MTdB', #12
        'https://open.kakao.com/o/gggxTdB', #13
        'https://open.kakao.com/o/g430TdB', #14
        'https://open.kakao.com/o/gHT9TdB', #15
        'https://open.kakao.com/o/gQhiUdB', #16
        'https://open.kakao.com/o/gTisUdB', #17
        'https://open.kakao.com/o/gHWCUdB', #18
    ]
    
    """     
    여분의 오픈채팅방
    'https://open.kakao.com/o/gQlJUdB', #19
    'https://open.kakao.com/o/gPRQUdB'  #20
    """

    subway = 0
    bus = 1
    
    #현재부터 1시간 이내 지하철 및 버스 스케쥴
    possibleSubwaySchedule = possibleScheduleCheck(subwaySchedule, subway)
    possibleRotateBusSchedule = possibleScheduleCheck(rotateBusSchedule, bus)
    possibleReturnBusSchedule = possibleScheduleCheck(returnBusSchedule, bus)

    
    #모든 지하철 도착 시간과 오픈채팅 연결
    matchAllScheduleRoom = matchAllScheduleWithRoom(subwaySchedule, chatRoom)
    
    #현재부터 1시간 이내 지하철 도착 시간과 연결된 오픈채팅 연결
    possibleSubwayScheduleRoom = matchPossibleScheduleWithRoom(possibleSubwaySchedule, matchAllScheduleRoom)
        
    return render(request, 'schedule/schedule_list.html', {'date': date, 
                                                           'day': day,
                                                           'subwaySchedule' : possibleSubwayScheduleRoom,
                                                           'rotateBusSchedule': possibleRotateBusSchedule,
                                                           'returnBusSchedule': possibleReturnBusSchedule })

#날짜 계산에 사용 
def days_hours_minutes(td):
    return [td.days, td.seconds//3600, (td.seconds//60)%60]

#현재 시각에서 1시간 이내 지하철 스케쥴 찾기
def possibleScheduleCheck(totalSchedule, transportKind):
    possibleSchedule = {}
    
    nowDateTime = datetime.datetime.now()

    for i, schedule in enumerate(totalSchedule):
        time = schedule.time
            
        #시간
        Time = datetime.date.today().strftime('%Y %m %d') + time
        
        ##현재 시간이 00시르 넘은 경우에 1일을 제한다.
        if datetime.datetime.now().strftime('%H') == '00':
            Time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y %m %d') + time
        
        DateTime = datetime.datetime.strptime(Time, '%Y %m %d%H %M')
        
        #시간 차이
        diffDateTime = DateTime - nowDateTime
        diffDateTimeArray = days_hours_minutes(diffDateTime)
        
        #00시 24시로 보정
        if time[0:2] == "00":
            diffDateTimeArray[0] = diffDateTimeArray[0] + 1

        diffHour = (diffDateTimeArray[0]*24*60 + diffDateTimeArray[1]*60 + diffDateTimeArray[2])/60
        
        #1시간 이내
        if diffHour >= 0:
            timeArray = time.split(' ')
            timeArray.insert(1, '시')
            if transportKind == 0: 
                timeArray.append('분 도착 오픈채팅방')
            else:
                timeArray.append('분')
            possibleSchedule[schedule] = (' '.join(timeArray))
            
    return possibleSchedule
    
#지하철 도착 시간과 오픈채팅방 연결
def matchAllScheduleWithRoom(subwaySchedule, chatRoom):
    match = {}
    
    #각 스케쥴에 방 3개씩 연결
    for i, time in enumerate(subwaySchedule):
        match[subwaySchedule[i]] = [chatRoom[(3*i)%len(chatRoom)], chatRoom[(3*i+1)%len(chatRoom)], chatRoom[(2*i+2)%len(chatRoom)]]
            
    return match
    
#1시간 이내 지하철 도착 시간과 오픈채팅방 연결
def matchPossibleScheduleWithRoom(possibleSubwaySchedule, matchAllScheduleRoom):
    possibleScheduleRoom = {}
    
    for key in matchAllScheduleRoom:
       if key in possibleSubwaySchedule:
           possibleScheduleRoom[key] = matchAllScheduleRoom[key]
    
    return possibleScheduleRoom
    
#schedule reserve
@login_required
@require_POST
def schedule_reserve(request):
    
    pk = request.POST.get('pk', None)
    schedule = get_object_or_404(Schedule, pk=pk)
    schedule_reserve, schedule_reserve_created = schedule.reserve_set.get_or_create(user=request.user)
    
    if not schedule_reserve_created:
        schedule_reserve.delete()
        message = "예약이 취소되었습니다."
        showMessage = "예약 하기"

    else:
        message = "예약이 완료되었습니다.\n\n오픈채팅방 링크를 클릭하시면 해당 시각의 택시 합승 방으로 연결됩니다."
        showMessage = "예약 취소"

    context = {
        'reserve_count': schedule.reserve_count,
        'message': message,
        'showMessage': showMessage
    }
    
    return HttpResponse(json.dumps(context), content_type="application/json")
    
#오늘이 휴일인가 확인하기
def holidayCheck(date):
    
    #2017년 남은 휴일
    holiday = ['10 09', '12 25']
    
    if date in holiday:
        return True
    else:
        return False
    

