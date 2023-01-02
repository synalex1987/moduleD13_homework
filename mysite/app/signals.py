import os
from random import randint
from django.shortcuts import redirect
from django.db.models.signals import pre_delete, post_save
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from .models import Announcement, Files, OneTimeCode, MyUser, Comments
from django.template.loader import render_to_string


@receiver(pre_delete, sender=Announcement)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    objFiles = Files.objects.filter(Announcement=instance)
    for file in objFiles:
        if os.path.isfile(file.File.path):
            os.remove(file.File.path)


@receiver(post_save, sender=MyUser)
def confirm_code_registration(sender, instance, created, **kwargs):
    if created:
        code_Obj = OneTimeCode.objects.create(User=instance)
        CodeAccepted = False
        while not CodeAccepted:
            rand_code = randint(1000, 9999)
            if not OneTimeCode.objects.filter(Code=rand_code).exists():
                CodeAccepted = True
                code_Obj.Code = rand_code
                code_Obj.save()

        html_content = render_to_string(
            'account/register_code_email.html',
            {
                'register_code': rand_code,
                'user': instance.username,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Код поддтверждения',
            from_email='nbvwzbaotjrclrbea@gmx.com',
            to=[instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            pass

    return redirect('/announce/')


@receiver(post_save, sender=Comments)
def email_response_to_user(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string(
            'announce/comment_added.html',
            {
                'post_id': instance.Announcement_id,
                'post_title': instance.Announcement.Announcement_title,
                'user': instance.Announcement.Announcement_author,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Комментарий к объявлению',
            body="",
            from_email='nbvwzbaotjrclrbea@gmx.com',
            to=[instance.Announcement.Announcement_author.email],
        )
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            pass
    else:
        if instance.Comment_accepted:
            html_content = render_to_string(
                'announce/comment_accepted.html',
                {
                    'post_id': instance.Announcement_id,
                    'post_title': instance.Announcement.Announcement_title,
                    'user': instance.User.username,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Комментарий к объявлению',
                from_email='Vnbvwzbaotjrclrbea@gmx.com',
                to=[instance.User.email],
            )
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                pass
