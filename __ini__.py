import requests, bs4, time, random, warnings, json, os


class instagram_bot:
	warnings.filterwarnings('ignore')

	def __init__(self, usernames=[], login_username='', login_password=''):
		self.posts, self.usernames, self.sleep, self.username, self.password, self.logged, self.session, self.rhx_gis, self.random_useragent, self.cookies, self.graph_id = [], usernames, lambda: time.sleep(delay / 5), login_username, login_password, False, requests.session(), None, lambda: random.choice([
				lambda: 'Mozilla/5.0 (Macintosh; Intel Mac OS X %s_%s_%s) AppleWebKit/%s.%s (KHTML, like Gecko) Chrome/%s.%s.%s.%s Safari/%s.%s' % (
					random.randint(1, 999), random.randint(1, 999), random.randint(1, 999), random.randint(1, 1000),
					random.randint(1, 9999), random.randint(1, 10000), random.randint(1, 10000),
					random.randint(1, 100000),
					random.randint(1, 100000), random.randint(1000, 9999), random.randint(1000, 9999)),
				lambda: 'Mozilla/%s (Windows NT %s; Win%s; x%s) AppleWebKit/%s (KHTML, like Gecko) Chrome/%s.%s.%s.%s Safari/%s.%s' % (
					random.randint(1, 999), random.randint(1, 999), random.randint(1, 999), random.randint(1, 1000),
					random.randint(1, 9999), random.randint(1, 10000), random.randint(1, 10000),
					random.randint(1, 100000),
					random.randint(1, 100000), random.randint(1000, 9999), random.randint(1000, 9999)),
				lambda: 'Mozilla/%s (Windows NT %s; WOW%s; rv:%s) Gecko/%s Firefox/%s' % (
					random.randint(1, 999), random.randint(1, 999), random.randint(1, 999),
					random.randint(1, 999), random.randint(10000000, 99999999), random.randint(1, 999)),
				lambda: 'Instagram %s.%s.%s Android (%s/%s.%s.%s; 480dpi; 1152x1920; Meizu; MX%s; mx4; mt%s; en_US)' % (
					random.randint(1, 99), random.randint(1, 99), random.randint(1, 99),
					random.randint(1, 99), random.randint(1, 99), random.randint(1, 99),
					random.randint(1, 99), random.randint(1000, 9999), random.randint(1000, 9999))]), None, None
		self.constants, self.main_request = {'Base_url': 'https://www.instagram.com/', 'login_url': 'https://www.instagram.com/accounts/login/ajax/'}, None
		self.local_time = time.localtime(time.time())
		self.path_dir = os.path.join(os.path.dirname(__file__), "%s.%s.%s" % (self.local_time.tm_year, self.local_time.tm_mon, self.local_time.tm_mday))
		if not os.path.isdir(self.path_dir):
			os.mkdir(self.path_dir)
		self.session.headers.update({'Referer': self.constants['Base_url']+str(random.uniform(0.0, 100000000.0)), 'User-Agent': 'Instagram %s.%s.%s (iPhone%s,%s; iPhone OS %s_%s_%s; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/%s+' % (random.randint(0, 99), random.randint(0, 99), random.randint(0, 99), random.randint(5, 100), random.randint(1, 10), random.randint(8, 10), random.randint(0, 100), random.randint(0, 100), random.randint(100, 1000))})

		def check_login():
			if os.path.isfile('new_cookies.txt'):
				self.session.cookies = requests.utils.cookiejar_from_dict(dict(x.split('=') for x in open(os.path.join(os.path.dirname(__file__), 'new_cookies.txt'),'r').read().split(';')))
				request = self.session.get('https://www.instagram.com')
				if 'logged-in' not in request.text:
					return False
				return True
			return False
		if check_login():
			self.logged = True
			print('Logged in from recent cookies')
		else:
			self.login()
		self.start_get_profile_posts()

	def get_shared_data(self, username=''):
		resp = self.session.get(self.constants['Base_url']+username)
		self.main_request = resp.text
		if resp.status_code == 200 and resp.text.__contains__('_sharedData'):
			return json.loads(resp.text.split('window._sharedData = ')[1].split(';</script>')[0])
		return None

	def login(self):
		self.session.cookies.set('ig_pr', '1')
		self.session.headers.update({'Referer': self.constants['Base_url']+str(random.uniform(0.0, 100000000.0)), 'User-Agent': 'Instagram %s.%s.%s (iPhone%s,%s; iPhone OS %s_%s_%s; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/%s+' % (random.randint(0, 99), random.randint(0, 99), random.randint(0, 99), random.randint(5, 100), random.randint(1, 10), random.randint(8, 10), random.randint(0, 100), random.randint(0, 100), random.randint(100, 1000))})
		request = self.session.get(self.constants['Base_url'])
		self.session.headers.update({'X-CSRFToken': request.cookies['csrftoken']})
		login_data = {'username': self.username, 'password': self.password}
		login = self.session.post(self.constants['login_url'], data=login_data, allow_redirects=True)
		self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
		self.cookies, login_json = login.cookies, json.loads(login.text)
		if login.status_code == 200 and login_json['authenticated']:
			self.logged = True
			self.rhx_gis = self.get_shared_data()['rhx_gis']
			open('new_cookies.txt', 'a+').write(';'.join(["%s=%s" % (key, value) for (key, value) in self.cookies.items()]))
		else:
			print("Wrong Username or Password. Terminated")
			os._exit(1)

	def get_profile_posts(self, username, path, check_update=False):
		json_data = self.get_shared_data(username)
		self.session.headers.update({'X-Requested-With': 'XMLHttpRequest', 'X-Instagram-GIS': self.rhx_gis, 'Referer': self.constants['Base_url']+username})
		graph_id_api = lambda: [x.split('",')[0] for x in self.session.get('https://www.instagram.com' + [x for x in
																								   [x for x in
																									bs4.BeautifulSoup(
																										self.session.get(self.constants['Base_url'] + username).text).find_all(
																										'script') if
																									x.get('src', None)]
																								   if
																								   'ProfilePageContainer' in
																								   x['src']][0]['src']).text.split(',queryId:"')[1:]][-2]
		user = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
		user_id, is_private, has_next_page, next_page_cursor, this_page_posts, file_writer = user['id'], user['is_private'], user['edge_owner_to_timeline_media']['page_info']['has_next_page'], user['edge_owner_to_timeline_media']['page_info']['end_cursor'], user['edge_owner_to_timeline_media']['edges'], open(path, 'a+')
		main_data = file_writer.read()
		if check_update:
			if file_writer.readline() == str({'id': this_page_posts[0]['node']['id'],
							'post_url': 'https://www.instagram.com/p/%s' % i['node']['shortcode']}):
				return 'There\'s no updates scraper will stop'
		if not is_private:
			for i in this_page_posts:
				data = str({'id': i['node']['id'],
							'post_url': 'https://www.instagram.com/p/%s' % i['node']['shortcode']})
				if data not in main_data:
					file_writer.write(data + "\n")
			if has_next_page:
				def scraper(next_page: str):
					api_url = 'https://www.instagram.com/graphql/query/?query_hash=%s&variables={"id":"%s","first":100,"after":"%s"}' % (
						graph_id_api(), user_id, next_page)
					resp = None
					try:
						self.session.cookies.clear_expired_cookies()
						requests_session = self.session.get(api_url)
						resp = requests_session
						time.sleep(random.uniform(1, 10))
						self.session.headers.update({'Cookie': ';'.join(
							["%s=%s" % (key, value) for (key, value) in self.session.cookies.items()])})
						posts_data = json.loads(requests_session.text)
						return posts_data['data']['user']['edge_owner_to_timeline_media']
					except Exception as e:
						if resp.status_code == 429:
							self.session = requests.session()
							self.login()
							scraper(next_page_cursor)
				data = scraper(next_page_cursor)
				if data:
					while has_next_page:
						for i in data['edges']:
							data_to_scrape = str({'id': i['node']['id'],
									 'post_url': 'https://www.instagram.com/p/%s' % i['node']['shortcode']})
							if data_to_scrape not in main_data:
								file_writer.write(data_to_scrape + "\n")
						next_page_cursor, has_next_page = data['page_info']['end_cursor'], data['page_info']['has_next_page']
						data = scraper(next_page_cursor)
						if not data:
							file_writer.close()
		file_writer.close()

	def start_get_profile_posts(self):
		if self.usernames and self.logged:
			for username in self.usernames:
				print('Scrapping %s' % username)
				self.get_profile_posts(username, os.path.join(self.path_dir, username))
			print("Done. You will find posts in %s" % self.path_dir)
