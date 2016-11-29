# review_demo
Review demo with a few models and small API

# Test
You can run test with default command:

    ./manage test

# Test data
You can load test data with:

    ./manage.py loaddata app/fixtures/test_data.json

# Admin panel with test data credentials
    user: admin
    pass: bairesdev

# Authentication
In order to authenticate the user I use django-tokenapi so in order to
use the api first you have to get tokej for instance

curl -d "username=pparker&password=spider123" http://www.yourdomain.com/token/new.json

#Create reviews Example using django client

    user, token = self.login_user('pparker', 'spider123')
    data = {
        'user': user,
        'token': token,
        'title': 'My review',
        'rating': 3,
        'summary': 'Great review bla bla bla',
        'company_id': 1,
    }

    response = self.client.post('/api/set_review', data)
    response_dict = json.loads(response.content)


# Get reviews example using django client

    user, token = self.login_user('ckent', 'spider123')
    data = {
        'user': user,
        'token': token,
    }

    response = self.client.post('/api/get_review_list', data)
    response_dict = json.loads(response.content)
