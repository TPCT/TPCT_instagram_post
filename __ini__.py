def Insta_Post_Links_list(username):
	import json, requests, time, random, bs4, warnings
	random_useragents =lambda: random.choice([
                 lambda: 'Mozilla/5.0 (Macintosh; Intel Mac OS X %s_%s_%s) AppleWebKit/%s.%s (KHTML, like Gecko) Chrome/%s.%s.%s.%s Safari/%s.%s'% (
					 random.randint(1, 999), random.randint(1, 999), random.randint(1, 999), random.randint(1, 1000),
					 random.randint(1, 9999), random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 100000),
					 random.randint(1, 100000), random.randint(1000, 9999), random.randint(1000, 9999)),
                 lambda: 'Mozilla/%s (Windows NT %s; Win%s; x%s) AppleWebKit/%s (KHTML, like Gecko) Chrome/%s.%s.%s.%s Safari/%s.%s' % (
					 random.randint(1, 999), random.randint(1, 999), random.randint(1, 999), random.randint(1, 1000),
					 random.randint(1, 9999), random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 100000),
					 random.randint(1, 100000), random.randint(1000, 9999), random.randint(1000, 9999)),
										  lambda: 'Mozilla/%s (Windows NT %s; WOW%s; rv:%s) Gecko/%s Firefox/%s' % (
										  random.randint(1, 999), random.randint(1, 999), random.randint(1, 999),
										  random.randint(1, 999), random.randint(10000000, 99999999), random.randint(1, 999)),
										  lambda: 'Instagram %s.%s.%s Android (%s/%s.%s.%s; 480dpi; 1152x1920; Meizu; MX%s; mx4; mt%s; en_US)' % (
										  random.randint(1, 99), random.randint(1, 99), random.randint(1, 99),
										  random.randint(1, 99), random.randint(1, 99), random.randint(1, 99),
										  random.randint(1, 99), random.randint(1000, 9999), random.randint(1000, 9999))])
	login_settings = {'username': 'ece86013b8@emailna.life', 'password': 'Th3@Professional'}
	warnings.filterwarnings('ignore')
	headers, session = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'accept-language': 'en-US,en;q=0.5',
		'Chache-Control': 'max-age=0',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'Host': 'www.instagram.com',
		'Cookie': '',
		'DNT': '%s' % random.randint(1, 10),
		'Referer': str('https://www.instagram.com/%s/' % username),
		'User-Agent': random_useragents()(),
		'Cookie2': '$Version=%s' % random.randint(1, 10),
		'Upgrade-Insecure-Requests': '1',
		'X-Instagram-AJAX': str(random.random()),
		'Content-Type': 'application/x-www-form-urlencoded',
		'x-requested-with': 'XMLHttpRequest'
	}, requests.session()
	request = session.get('https://www.instagram.com/accounts/login/?force_classic_login')
	csrf_token = request.cookies['csrftoken']
	session.headers.update({'X-CSRFToken': csrf_token})
	login = session.post('https://www.instagram.com/accounts/login/?force_classic_login', data=login_settings,
						 allow_redirects=True)
	session.headers.update(headers)
	request = session.get('https://www.instagram.com/%s/?en&hl=en' % username)
	if 'error-container' in request.text:
		return 'Wrong username or password'
	session.headers.update({'X-CSRFToken': csrf_token})
	json_load = (request.text.split('window._sharedData = ')[1].split('<')[0].encode(errors='ignore').decode(
		errors='ignore')).replace(';', '')
	json_load = json.loads(json_load)
	new_cookies = lambda: ';'.join(['%s=%s' % (key, value) for (key, value) in session.cookies.items()])
	session.headers['Cookie'] = new_cookies()
	user = json_load['entry_data']['ProfilePage'][0]['graphql']['user']
	user_id = user['id']
	has_next_page = user['edge_owner_to_timeline_media']['page_info']['has_next_page']
	next_page_cursor = user['edge_owner_to_timeline_media']['page_info']['end_cursor']
	posts_data = []
	if has_next_page:
		api_access = session.get('https://www.instagram.com' + [x for x in [x for x in
																			bs4.BeautifulSoup(request.text).find_all(
																				'script') if x.get('src', None)] if
																'ProfilePageContainer' in x['src']][0]['src'])
		session.headers.update({'X-CSRFToken': csrf_token})
		api_access = [x.split('",')[0] for x in api_access.text.split(',queryId:"')[1:]][-2]
		def scraper(next_page: str):
			try:
				api_url = 'https://www.instagram.com/graphql/query/?query_hash=%s&variables={"id":"%s","first":100,"after":"%s"}' % (
					api_access, user_id, next_page)
				time.sleep(5 * random.uniform(0.0, 2.0))
				session.headers['User-Agent'] = random_useragents()()
				session.headers['Cookie'] = new_cookies()
				return json.loads(session.get(api_url).text)['data']['user']['edge_owner_to_timeline_media']
			except Exception as e:
				return None
		data = scraper(next_page_cursor)
		if data:
			while has_next_page:
				for i in data['edges']:
					posts_data.append(
						{'id': i['node']['id'], 'post_url': 'https://www.instagram.com/p/%s' % i['node']['shortcode']})
				next_page_cursor, has_next_page = data['page_info']['end_cursor'], data['page_info']['has_next_page']
				data = scraper(next_page_cursor)
				if not data:
					return posts_data
		else:
			return 'Please Enter New Username and Password'
	else:
		for i in user['edge_owner_to_timeline_media']['edges']:
			posts_data.append(
				{'id': i['node']['id'], 'post_url': 'https://www.instagram.com/p/%s' % i['node']['shortcode']})
	return posts_data
