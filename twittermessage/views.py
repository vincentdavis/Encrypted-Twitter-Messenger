from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from twython import Twython



def home(request):
    #OAUTH_TOKEN = settings.getattr('OAUTH_TOKEN')
    #OAUTH_TOKEN_SECRET = settings.getattr('OAUTH_TOKEN_SECRET')

    if request.session.get('latest_token', False):
        return HttpResponseRedirect('/account/')

    twitter = Twython(settings.APP_KEY, settings.APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

    request.session['OAUTH_TOKEN']=OAUTH_TOKEN
    request.session['OAUTH_TOKEN_SECRET'] = OAUTH_TOKEN_SECRET
    auth_url = auth['auth_url']

    return redirect(auth_url)


def twitterapi(request):
    oauth_verifier = request.GET.get('oauth_verifier',None)
    oauth_token = request.GET.get('oauth_token', None)

    twitter = Twython(
            settings.APP_KEY,
            settings.APP_SECRET,
            request.session['OAUTH_TOKEN'],
            request.session['OAUTH_TOKEN_SECRET']
            )
    final_step = twitter.get_authorized_tokens(oauth_verifier)

    OAUTH_TOKEN = final_step['oauth_token']
    OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

    request.session['OAUTH_TOKEN']=OAUTH_TOKEN
    request.session['OAUTH_TOKEN_SECRET'] = OAUTH_TOKEN_SECRET

    if OAUTH_TOKEN  and OAUTH_TOKEN_SECRET:
        request.session['latest_token']=True
    return HttpResponseRedirect('/account/')


def get_twitter_instance(request):
    twitter = Twython(
            settings.APP_KEY,
            settings.APP_SECRET,
            request.session['OAUTH_TOKEN'],
            request.session['OAUTH_TOKEN_SECRET']
            )
    return twitter
    
def twitter_search(twitter,search=''):
    results = twitter.search(q=search)
    res = []
    for result in results['statuses']:
        res.append({'name': result['user']['name'],'text': result['text']})
    return res

def user_account(request):
    ctx = {}
    search =  request.GET.get('search', False)
    status = request.GET.get('status', False)
    twitter = get_twitter_instance(request)
    if search:
        searchs = twitter_search(twitter, search)
        ctx.update({'searchs':searchs})
    if status:
        twitter.update_status(status=status)
        ctx.update({'status_msg':status+" updated!!"})

    tweets = twitter.get_home_timeline()
    my_tweets = []

    for tweet in tweets:
        my_tweets.append({
            'created':tweet['created_at'],
            'text':tweet['text'],
            'retweet_count':tweet['retweet_count']
            })
    ctx.update({'my_tweets':my_tweets})

    ctx.update({'user':{
            'user':tweets[0]['user']['name'], 
            'profile_pic':tweets[0]['user']['profile_image_url_https']
            }
        })


    return render(request,"index.html", ctx)
