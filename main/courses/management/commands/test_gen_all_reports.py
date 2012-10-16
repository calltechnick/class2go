from django.core.management.base import BaseCommand, CommandErrorfrom c2g.models import *from django.contrib.auth.models import User,Groupfrom django.db import connection, transactionfrom datetime import datetime, timedeltafrom courses.reports.generation.gen_course_dashboard_report import *from courses.reports.generation.gen_quiz_summary_report import *from courses.reports.generation.gen_quiz_full_report import *class Command(BaseCommand):    help = "Test generate one instance of every possible report\n"            def handle(self, *args, **options):        now = datetime.now()        active_courses = Course.objects.filter(mode='ready', calendar_end__gt=now)                save_to_s3 = True                for ready_course in active_courses:            # Generate course dashboard report            report = gen_course_dashboard_report(ready_course, save_to_s3)            if save_to_s3:                if report['path']: print "Report successfully written to: %s" % report['path']                else: print "Failed to generate report or write it to S3!"                            # Generate Courser quizzes summary report            report = gen_course_quizzes_report(ready_course, save_to_s3)            if save_to_s3:                if report['path']: print "Report successfully written to: %s" % report['path']                else: print "Failed to generate report or write it to S3!"                            # Video reports            videos = Video.objects.getByCourse(course=ready_course).order_by('-live_datetime')                        for ready_quiz in videos:                report = gen_quiz_full_report(ready_course, ready_quiz, save_to_s3)                if save_to_s3:                    if report['path']: print "Report successfully written to: %s" % report['path']                    else: print "Failed to generate report or write it to S3!"                                    report = gen_quiz_summary_report(ready_course, ready_quiz, save_to_s3)                if save_to_s3:                    if report['path']: print "Report successfully written to: %s" % report['path']                    else: print "Failed to generate report or write it to S3!"                                # Problemsets            problem_sets = ProblemSet.objects.getByCourse(course=ready_course).order_by('-live_datetime')            for ready_quiz in videos:                report = gen_quiz_full_report(ready_course, ready_quiz, save_to_s3)                if save_to_s3:                    if report['path']: print "Report successfully written to: %s" % report['path']                    else: print "Failed to generate report or write it to S3!"                                    report = gen_quiz_summary_report(ready_course, ready_quiz, save_to_s3)                if save_to_s3:                    if report['path']: print "Report successfully written to: %s" % report['path']                    else: print "Failed to generate report or write it to S3!"            