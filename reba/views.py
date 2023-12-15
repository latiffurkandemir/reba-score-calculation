from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reba
from django.contrib.staticfiles.views import serve
import xlwt
from django.http import HttpResponse

def home(request):
    return render(request, 'reba/home.html')

@login_required
def rebaWithoutVideo(request):
    return render(request, 'reba/rebaWithoutVideo.html')

@login_required
def rebaWithVideo(request):
    return render(request, 'reba/rebaWithVideo.html')

def rebaResults(request):
    context = {}
    if request.method == "POST":
        table_A = [[[1, 2, 3, 4], [2, 3, 4, 5], [2, 4, 5, 6], [3, 5, 6, 7], [4, 6, 7, 8]],
                [[1, 2, 3, 4], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9]],
                [[3, 3, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9], [7, 8, 9, 9]]]

        table_B = [[[1, 2, 2], [1, 2, 3]],
                [[1, 2, 3], [2, 3, 4]],
                [[3, 4, 5], [4, 5, 5]],
                [[4, 5, 5], [5, 6, 7]],
                [[6, 7, 8], [7, 8, 8]],
                [[7, 8, 8], [8, 9, 9]],]

        table_C = [[1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7],
                [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8],
                [2, 3, 3, 3, 4, 5, 6, 7, 7, 8, 8, 8],
                [3, 4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9],
                [4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9, 9],
                [6, 6, 6, 7, 8, 8, 9, 9, 10, 10, 10, 10],
                [7, 7, 7, 8, 9, 9, 9, 10, 10, 11, 11, 11],
                [8, 8, 8, 9, 10, 10, 10, 10, 10, 11, 11, 11],
                [9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12],
                [10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 12],
                [11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12],
                [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],]
        
        # Table A
        neck_position = int(request.POST.get('neck_position'))
        neck_adjustment = 0
        if(request.POST.get('neck_adjustment')):
            neck_adjustment = int(request.POST.get('neck_adjustment'))
            neck_score = neck_position + neck_adjustment
        else:
            neck_score = neck_position

        trunk_position = int(request.POST.get('trunk_position'))
        trunk_adjustment = 0
        if(request.POST.get('trunk_adjustment')):
            trunk_adjustment = int(request.POST.get('trunk_adjustment'))
            trunk_score = trunk_position + trunk_adjustment
        else:
            trunk_score = trunk_position

        leg_position = int(request.POST.get('leg_position'))
        leg_adjustments = 0
        if(request.POST.get('leg_adjustments')):
            leg_adjustments = int(request.POST.get('leg_adjustments'))
            leg_score = leg_position + leg_adjustments
        else:
            leg_score = leg_position

        posture_score_A = table_A[neck_score-1][trunk_score-1][leg_score-1]

        force_load = int(request.POST.get('force_load'))
        force_load2 = 0
        if(request.POST.get('force_load2')):
            force_load2 = int(request.POST.get('force_load2'))

        score_A = posture_score_A + force_load + force_load2

        # Table B
        upper_arm_position = int(request.POST.get('upper_arm_position'))
        upper_arm_score = upper_arm_position
        if(request.POST.get('upper_arm_adjustment1')):
            upper_arm_adjustment1 = int(request.POST.get('upper_arm_adjustment1'))
            upper_arm_score += upper_arm_adjustment1
        if(request.POST.get('upper_arm_adjustment2')):
            upper_arm_adjustment2 = int(request.POST.get('upper_arm_adjustment2'))
            upper_arm_score += upper_arm_adjustment2
        if(request.POST.get('upper_arm_adjustment3')):
            upper_arm_adjustment3 = int(request.POST.get('upper_arm_adjustment3'))
            upper_arm_score += upper_arm_adjustment3

        lower_arm_position = int(request.POST.get('lower_arm_position'))

        wrist_position = int(request.POST.get('wrist_position'))
        wrist_score = wrist_position
        if(request.POST.get('wrist_adjustment')):
            wrist_adjustment = int(request.POST.get('wrist_adjustment'))
            wrist_score += wrist_adjustment
        
        posture_score_B = table_B[upper_arm_score-1][lower_arm_position-1][wrist_score-1]

        coupling = int(request.POST.get('coupling'))

        score_B = posture_score_B + coupling

        # Table C and final reba score
        score_C = table_C[score_A-1][score_B-1]

        final_reba_score = score_C
        if(request.POST.get('activity_score1')):
            activity_score1 = int(request.POST.get('activity_score1'))
            final_reba_score += activity_score1
        if(request.POST.get('activity_score2')):
            activity_score2 = int(request.POST.get('activity_score2'))
            final_reba_score += activity_score2
        if(request.POST.get('activity_score3')):
            activity_score3 = int(request.POST.get('activity_score3'))
            final_reba_score += activity_score3

        # Result text
        if final_reba_score == 1:
            result_text = "Negligible risk"
        elif final_reba_score == 2 or final_reba_score == 3:
            result_text = "Low risk, change may be needed"
        elif final_reba_score > 3 and final_reba_score < 8:
            result_text = "Medium risk, further investigation, change soon"
        elif final_reba_score > 7 and final_reba_score < 11:
            result_text = "High risk, investigate and implement change"
        else:
            result_text = "Very high risk, implement change"

        context['result_text'] = result_text
        context['final_score'] = final_reba_score

        # Save the model (Reba) if user is logged in
        if request.user.is_authenticated:
            reba_object = Reba.objects.create(
                userID = request.user,

                neckPosition = neck_position,
                neckAdjust = neck_adjustment,
                neckScore = neck_score,

                trunkPosition = trunk_position,
                trunkAdjust = trunk_adjustment,
                trunkScore = trunk_score,

                legPosition = leg_position,
                legAdjust = leg_adjustments,
                legScore = leg_score,

                postureScoreA = posture_score_A,
                flScore = force_load + force_load2,
                scoreA = score_A,

                upperArmPosition = upper_arm_position,
                upperArmAdjust = upper_arm_score - upper_arm_position,
                upperArmScore = upper_arm_score,

                lowerArmPosition = lower_arm_position,
                lowerArmScore = lower_arm_position,

                wristPosition = wrist_position,
                wristAdjust = wrist_score - wrist_position,
                wristScore = wrist_score,

                postureScoreB = posture_score_B,
                
                couplingScore = coupling,

                scoreB = score_B,

                tableScoreC = score_C,

                activityScore = final_reba_score - score_C,

                finalRebaScore = final_reba_score,
            )

    return render(request, 'reba/rebaResults.html', context)
   
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reba.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Reba')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Reba ID', 'User ID', 'Neck Position', 'Neck Adjust', 'Neck Score', 'Trunk Position', 'Trunk Adjust',
               'Trunk Score', 'Leg Position' , 'Leg Adjust', 'Leg Score', 'Posture Score A', 'Force Load Score',
               'Score A', 'Upper Arm Position', 'Upper Arm Adjust', 'Upper Arm Score',
               'Lower Arm Position', 'Lower Arm Score', 'Wrist Position', 'Wrist Adjust',
               'Wrist Score', 'Posture Score B', 'Coupling Score', 'Score B' ,'Table Score C',
               'Activity Score' ,'Final Reba Score']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    user = request.user
    rows = Reba.objects.filter(userID = user.id).values()
    for index_row, row in enumerate(rows):
        for index_col, key in enumerate(row):
            ws.write(index_row+1, index_col, row[key], font_style)

    wb.save(response)
    return response

def getfile(request):
   return serve(request, 'File')

def about(request):
    return render(request, 'reba/about.html', {'title': 'About'})
