import base64
import time
from django.http import HttpResponse, HttpResponseNotFound
from mongoengine.queryset.visitor import Q
import json
# Create your views here.

from wenba_back.models import ArticleDetail, ArticleIndex, User, Comment


def parseArticleIndex(article):
    temp_list = {'_id': article._id, 'period': article.period, 'title': article.title,
                 'author': article.author, 'desc': article.desc, 'browse_num': article.browse_num,
                 'comment_num': article.comment_num, 'preview': article.preview, 'link': article.link}
    return temp_list


def parseComment(comment):
    temp_list = {'_id': comment._id, 'author_id': comment.author_id,
                 'content': comment.content, 'text_content': comment.text_content, 'reply': comment.reply,
                 'created': comment.created, 'is_main': comment.is_main, 'approve_num': comment.approve_num,
                 'browse_num': comment.browse_num, 'approved_usr_ids': comment.approved_user_ids}
    return temp_list


def getImageUrl(image):
    image = base64.b64encode(image)
    image = bytes.decode(image)
    return 'data:image/jpeg;base64,' + image


def parseUser(user):
    temp_list = {'email': user._id, 'username': user.username, 'password': user.password, 'avatarUrl': user.avatarUrl}

    return temp_list


def detail(request):
    """

    :param request:
    :return:
    """
    article_id = 0
    if request.method == 'GET':
        article_id = int(request.GET.get('id', 0))
    elif request.method == 'POST':
        article_id = int(request.POST.get('id', 0))
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if article_id != 0:
        try:
            article = ArticleDetail.objects.get(_id=article_id)
        except Exception as e:
            print(e)
            return HttpResponseNotFound('none')
        temp_list = {'_id': article._id, 'period': article.period, 'title': article.title,
                     'author': article.author, 'desc': article.desc, 'browse_num': article.browse_num,
                     'comment_num': article.comment_num, 'preview': article.preview, 'link': article.link,
                     'figure': article.figure, 'inside_title': article.inside_title, 'fav_num': article.fav_num,
                     'approve_num': article.approve_num, 'content': article.content, 'date': article.date}
        return_data = json.dumps(temp_list, ensure_ascii=False)

        return HttpResponse(return_data, content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': 'id不存在'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")


def index(request):
    """

    :param request:
    :return:
    """
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if page != 0:
        articles = ArticleIndex.objects.order_by('-period')[(page - 1) * 10: page * 10]
        return_data = []
        for article in articles:
            return_data.append(parseArticleIndex(article))
        return_data = json.dumps(return_data)
        return HttpResponse(return_data, content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '未知错误'}, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")


def addbrowsenum(request):
    """

    :param request:
    :return:
    """
    article_id = 0
    if request.method == "GET":
        article_id = request.GET.get('id', 0)
    elif request.method == "POST":
        article_id = request.POST.get('id', 0)
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if article_id != 0:
        article = ArticleDetail.objects.get(_id=article_id)
        article_index = ArticleIndex.objects.get(_id=article_id)
        article.browse_num += 1
        article_index.browse_num += 1
        article.save()
        article_index.save()
        message = {
            'result': 1,
            'reason': '阅读量+1'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        message = {
            'result': 0,
            'reason': '请求方式错误！'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")


def addapprovenum(request):
    """

    :param request:
    :return:
    """
    if request.method == "GET":
        article_id = request.GET.get('id', 0)
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if article_id:
        article = ArticleDetail.objects.get(_id=article_id)
        article.approve_num += 1
        article.save()
        message = {
            'result': 1,
            'reason': '点赞量+1'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        message = {
            'result': 0,
            'reason': '请求方式错误！'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")


def addfav(request):
    """

    :param request:
    :return:
    """
    article_id = 0
    user_id = 0
    if request.method == "GET":
        article_id = request.GET.get('id', 0)
        user_id = request.GET.get('user_id', '0')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if article_id != 0 and user_id != '0':
        # print('article_id', article_id, '  user_id', user_id)
        article = ArticleDetail.objects.get(_id=article_id)
        user = User.objects.get(_id=user_id)
        user.fav_list.append(article_id)
        user.save()
        article.fav_num += 1
        article.save()
        message = {
            'result': 1,
            'reason': '收藏量+1'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        message = {
            'result': 0,
            'reason': '请求方式错误！'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")


def reducefav(request):
    """

    :param request:
    :return:
    """
    article_id = 0
    user_id = 0
    if request.method == "GET":
        article_id = request.GET.get('id', 0)
        user_id = request.GET.get('user_id', 0)
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if article_id != 0 and user_id != 0:
        article = ArticleDetail.objects.get(_id=article_id)
        article.fav_num -= 1
        user = User.objects.get(_id=user_id)
        while article_id in user.fav_list:
            user.fav_list.remove(article_id)
        user.save()
        article.save()
        message = {
            'result': 1,
            'reason': '收藏量-1'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        message = {
            'result': 0,
            'reason': '请求方式错误！'
        }
        return HttpResponse(json.dumps(message, ensure_ascii=False), content_type="application/json,charset=utf-8")


def register(request):
    """

    :param request:
    :return:
    """
    username = ''
    password = ''
    email = ''
    if request.method == "GET":
        username = request.GET.get('username', '')
        password = request.GET.get("password", '')
        email = request.GET.get('email', '')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    user_count = len(User.objects.all()) + 1
    user = User()
    user.password = password
    user.username = username
    user._id = email
    old_user = User.objects.all().filter(_id=email).first()
    if old_user:
        return HttpResponse(json.dumps(
            {'result': 0, 'reason': 'Email {} already exists!'.format(email)}, ensure_ascii=False),
            content_type='application/json,charset=utf-8')
    else:
        user.save()
        return HttpResponse(json.dumps(
            {'result': 1, 'user_count': user_count, 'reason': 'add User {} successfully'.format(username)},
            ensure_ascii=False),
            content_type='application/json,charset=utf-8')


def login(request):
    """
    :param request:
    :return:
    """
    if request.method == "GET":
        username = str(request.GET.get('username', ''))
        email = request.GET.get('email', '')
        password = str(request.GET.get('password', ''))
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')

    # print('email', email, 'username', username, 'password', password)
    if username != '':
        user = User.objects(Q(username=username) & Q(password=password)).first()
        if user:
            return HttpResponse(
                json.dumps({'result': 1, 'reason': '登录成功', 'userInfo': parseUser(user)}, ensure_ascii=False),
                content_type='application/json,charset=utf-8')
        else:
            return HttpResponse(json.dumps({'result': 0, 'reason': '登录失败'}, ensure_ascii=False),
                                content_type='application/json,charset=utf-8')
    # 通过email进行登录
    else:
        user = User.objects.all().filter(_id=email).filter(password=password).first()
        if user:
            return HttpResponse(
                json.dumps({'result': 1, 'reason': '登录成功', 'userInfo': parseUser(user)}, ensure_ascii=False),
                content_type='application/json,charset=utf-8')
        else:
            return HttpResponse(json.dumps({'result': 0, 'reason': '登录失败'}, ensure_ascii=False),
                                content_type='application/json,charset=utf-8')


def changeavatar(request):
    if request.method == 'POST':
        post_body = request.body
        post_body = json.loads(post_body)
        avatarUrl = post_body.get('avatarUrl', '')
        user_id = post_body.get('user_id', '')
        user = User.objects(_id=user_id).first()
        if user:
            user.avatarUrl = avatarUrl
            user.save()
            return HttpResponse(
                json.dumps({'result': 1, 'reason': '头像更换成功', 'avatarUrl': avatarUrl}, ensure_ascii=False),
                content_type='application/json,charset=utf-8')
        else:
            return HttpResponse(json.dumps({'result': 0, 'reason': '用户不合法'}, ensure_ascii=False),
                                content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '上传失败'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')


def search(request):
    if request.method == "GET":
        value = request.GET.get('value', '')
    elif request.method == "POST":
        value = request.POST.get("value", '')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求方式错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    articles = ArticleIndex.objects(Q(title__icontains=value) | Q(author__icontains=value))
    return_data = []
    for article in articles:
        return_data.append(parseArticleIndex(article))
    count = len(return_data)
    # print('count: ', count)
    return HttpResponse(json.dumps(return_data, ensure_ascii=False), content_type='application/json,charset=utf-8')


def getfavs(request):
    if request.method == "GET":
        user_id = request.GET.get('user_id', 0)
    elif request.method == "POST":
        user_id = request.POST.get("user_id", 0)
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求方式错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if user_id != "":
        user = User.objects.get(_id=user_id)
        # print('user_id: ', user_id)
        favs = user.fav_list
        # print(favs)
        return_data = []
        articles = ArticleIndex.objects.all()
        for article_id in favs:
            return_data.append(parseArticleIndex(articles.get(_id=article_id)))
        return HttpResponse(
            json.dumps({'result': 1, 'articles': return_data, 'reason': '获得收藏文章成功！'}, ensure_ascii=False),
            content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(
            json.dumps({'result': 0, 'reason': "可能用户ID有误"}, ensure_ascii=False),
            content_type='application/json,charset=utf-8')


def judgeisfav(request):
    if request.method == "GET":
        article_id = request.GET.get('article_id', 0)
        user_id = request.GET.get('user_id', 0)
    elif request.method == "POST":
        article_id = request.POST.get('article_id', 0)
        user_id = request.POST.get('user_id', 0)
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if article_id != 0 and user_id != 0:
        # print(article_id, '  ', user_id)
        # print(type(user_id))
        favs = User.objects.get(_id=user_id).fav_list
        if article_id in favs:
            is_fav = True
        else:
            is_fav = False
        return HttpResponse(json.dumps({'result': 1, 'is_fav': is_fav, 'reason': '成功'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(
            json.dumps({'result': 0, 'reason': "用户ID或者文章ID有误"}, ensure_ascii=False),
            content_type='application/json,charset=utf-8')


def addcomment(request):
    if request.method == "POST":
        post_body = request.body
        data = json.loads(post_body)
        author_id = data.get('author_id', '')
        author_name = data.get('author_name', '')
        content = data.get('content', '')
        text_content = data.get('text_content', '')
        print(author_id, content, text_content, author_name)
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if author_id and content and author_name:
        comment = Comment()
        comment.author_id = author_id
        comment.content = content
        comment._id = author_id + str(time.time())
        comment.is_main = True
        comment.created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        comment.text_content = text_content
        comment.author_name = author_name
        comment.save()
        print('comment.save()')
        return HttpResponse(json.dumps({'result': 1, 'reason': '发布成功'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '发布失败'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')


def addreply(request):
    if request.method == "POST":
        post_body = request.body
        data = json.loads(post_body)
        author_id = data.get('author_id', '')
        content = data.get('content', '')
        comment_id = data.get('comment_id', '')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if author_id and content and comment_id:
        comment = Comment()
        comment.author_id = author_id
        comment.content = content
        comment.text_content = content
        comment._id = author_id + str(time.time())
        comment.is_main = False
        comment.created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        comment.reply = comment_id
        comment.save()
        return HttpResponse(json.dumps({'result': 1, 'reason': '评论成功'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '评论失败'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')


def getcomments(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 0))
        row = int(request.GET.get('row', 0))
        user_id = request.GET.get('user_id', '')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if page != 0 and row != 0:
        total_comments = Comment.objects.order_by('-created')
        total_users = User.objects
        comments = total_comments.filter(is_main=True)
        comments = comments[(page - 1) * row:page * row]
        return_data = []
        for comment in comments:
            comment['browse_num'] += 1
            comment.save()
            temp = parseComment(comment)
            if user_id in comment.approved_user_ids:
                temp['is_approved'] = True
            else:
                temp['is_approved'] = False
            approved_users = []
            for id in comment.approved_user_ids:
                user = total_users.get(_id=id)
                approved_users.append(user.username)
            temp['approved_users'] = approved_users
            temp['author'] = parseUser(total_users.get(_id=comment.author_id))
            replies = total_comments.order_by('created').filter(is_main=False).filter(reply=comment._id)
            comment_replies = []
            if replies:
                for reply in replies:
                    temp_reply = {'username': total_users.get(_id=reply.author_id).username, 'content': reply.content}
                    comment_replies.append(temp_reply)
            temp['replies'] = comment_replies
            return_data.append(temp)
        return HttpResponse(json.dumps(return_data, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')


def approvecomment(request):
    user_id = ''
    comment_id = ''
    if request.method == 'GET':
        user_id = request.GET.get('user_id', '')
        comment_id = request.GET.get('comment_id', '')
    if user_id and comment_id:
        comment = Comment.objects.get(_id=comment_id)
        comment['approve_num'] += 1
        comment['approved_user_ids'].append(user_id)
        comment.save()
        return_data = {'result': 1, 'reason': '点赞成功！'}
        return HttpResponse(json.dumps(return_data, ensure_ascii=False), content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')


def cancelapprovecomment(request):
    user_id = ''
    comment_id = ''
    if request.method == 'GET':
        user_id = request.GET.get('user_id', '')
        comment_id = request.GET.get('comment_id', '')
    if user_id and comment_id:
        comment = Comment.objects.get(_id=comment_id)
        comment['approve_num'] -= 1
        while user_id in comment.approved_user_ids:
            comment['approved_user_ids'].remove(user_id)
        comment.save()
        return_data = {'result': 1, 'reason': '取消点赞成功！'}
        return HttpResponse(json.dumps(return_data, ensure_ascii=False), content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')


def comsearch(request):
    if request.method == 'GET':
        value = request.GET.get('value', '')
        user_id = request.GET.get('user_id', '')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if value and user_id:
        total_comments = Comment.objects.order_by('-created')
        total_users = User.objects
        comments = total_comments.filter(is_main=True)
        comments = comments.filter(Q(text_content__icontains=value) | Q(author_name__icontains=value))
        return_data = []
        for comment in comments:
            comment['browse_num'] += 1
            comment.save()
            temp = parseComment(comment)
            if user_id in comment.approved_user_ids:
                temp['is_approved'] = True
            else:
                temp['is_approved'] = False
            approved_users = []
            for id in comment.approved_user_ids:
                user = total_users.get(_id=id)
                approved_users.append(user.username)
            temp['approved_users'] = approved_users
            temp['author'] = parseUser(total_users.get(_id=comment.author_id))
            replies = total_comments.order_by('created').filter(is_main=False).filter(reply=comment._id)
            comment_replies = []
            if replies:
                for reply in replies:
                    temp_reply = {'username': total_users.get(_id=reply.author_id).username, 'content': reply.content}
                    comment_replies.append(temp_reply)
            temp['replies'] = comment_replies
            return_data.append(temp)
        return HttpResponse(json.dumps(return_data, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')


def getmycomments(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id', '')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    if user_id:
        total_comments = Comment.objects.order_by('-created')
        total_users = User.objects
        comments = total_comments.filter(is_main=True).filter(author_id=user_id)
        return_data = []
        for comment in comments:
            comment['browse_num'] += 1
            comment.save()
            temp = parseComment(comment)
            if user_id in comment.approved_user_ids:
                temp['is_approved'] = True
            else:
                temp['is_approved'] = False
            approved_users = []
            for id in comment.approved_user_ids:
                user = total_users.get(_id=id)
                approved_users.append(user.username)
            temp['approved_users'] = approved_users
            temp['author'] = parseUser(total_users.get(_id=comment.author_id))
            replies = total_comments.order_by('created').filter(is_main=False).filter(reply=comment._id)
            comment_replies = []
            if replies:
                for reply in replies:
                    temp_reply = {'username': total_users.get(_id=reply.author_id).username, 'content': reply.content}
                    comment_replies.append(temp_reply)
            temp['replies'] = comment_replies
            return_data.append(temp)
        return HttpResponse(json.dumps(return_data, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 0, 'reason': '请求错误'}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8')
