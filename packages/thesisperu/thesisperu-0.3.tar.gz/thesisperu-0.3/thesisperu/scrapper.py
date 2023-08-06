import requests as r
from bs4 import BeautifulSoup as bs
import numpy as np, pandas as np
import tqdm, warnings, re
# from dataclasses import dataclass

warnings.filterwarnings('ignore')

def get_html(url, element='div', css = 'artifact-description'):
	response = r.get(url, verify=False).content
	html = bs(response, 'html.parser')
	s_items = html.find_all(element, class_ = css)
	# return a sublinks 
	return s_items

def get_main_items(sub_items, master_dir = '', prefix = None):

	if prefix is None:
		raise "No Prefix provided"

	urls, num_thesis, name_links = [], [], []
	sub_items_df = pd.DataFrame()

	for item in sub_items:
		master = item.find('h4') # titles and sublinks	
		# name sublinks
		sublinks = prefix + master.find('a')['href'] # link
		subitem = master.find('span').string # name

		text_without_spaces = re.sub('[\s\t]+', '', subitem)
		name_len_text = len(text_without_spaces)

		if name_len_text < 3:
			continue

		try:
			sub_text_number = master.getText() 
			n_tesis = re.search(r'\[(\d+)\]', sub_text_number).group(1)
			n_tesis = int(n_tesis)
		except:
			n_tesis = 0
		
		urls.append(sublinks)
		name_links.append(subitem)
		num_thesis.append(n_tesis)

	sub_items_df = sub_items_df.assign(
		dir_name = name_links, num_thesis = num_thesis, urls = urls,
		master_dir = master_dir
	)
	return sub_items_df

def search_sub_items(main_items_df):
	urls = main_items_df.urls.to_numpy()
	name = main_items_df.dir_name.to_numpy()
	sub_df = pd.DataFrame()

	for i, url in tqdm.tqdm(enumerate(urls)):
		sub_url_df = get_main_items(get_html(url), name[i])
		sub_df = pd.concat((sub_df, sub_url_df))
	return sub_df


def get_thesis_metadata(url, master_dir='dir', sub_dir='sdir', prefix=None):
	response = r.get(url, verify=False).content
	meta_url = bs(response, 'html.parser')
	table = str(meta_url.find('table'))
	df = pd.read_html(str(table))[0][[0, 1]]
	df = df.groupby(0, as_index=False).agg("\n".join)
	df = df.set_index(0).T.reset_index().drop(columns=["index"])

	# pdf link search by sequence={1, 3, 4, 10}
	pdf_div = meta_url.find_all('div', class_ = 'file-link')
	# l_div = len(pdf_div)
	pdf_ = list(np.repeat([np.nan], 4))

	for i, div in enumerate(pdf_div):
		if i > 4:
			continue
		try:
			ref_a = div.find('a')
			try:
				ref = ref_a['href'] # h ref tesis pdf
				pdf_[i] = prefix + ref
			except:
				pass
		except:
			pass
			
	pdf_ref = {
		'url_metadata': [url], 'pdf_0': [pdf_[0]], 'pdf_1': [pdf_[1]],
		'pdf_2': [pdf_[2]], 'pdf_3': [pdf_[3]], 'master_dir': [master_dir], 
		'sub_dir': [sub_dir]
	}
	pdf_df_ref = pd.DataFrame(pdf_ref)
	df1 = pd.concat((df, pdf_df_ref), axis = 1)
	return df1


def get_thesis_by_subitems(url, master_dir, sub_dir, prefix=None):
	thesis_find = get_html(url, 'h4', 'artifact-title')
	thesis_find_df = pd.DataFrame()
	link = []
	for i, thesis in enumerate(thesis_find):
		href = thesis.find('a')['href']
		metadata_url = prefix + href + "?show=full"
		link.append(metadata_url)

		thesis_df = get_thesis_metadata(metadata_url, master_dir, sub_dir, prefix=prefix)
		thesis_find_df = pd.concat((thesis_df_info, thesis_df))
	return thesis_find_df

def progress(i, n):
	percent = np.round(i / n * 100) 
	return percent

def download_metadata_less20(df):
	master_dirs = df.master_dir.to_numpy()
	sub_dirs = df.dir_name.to_numpy()
	urls = df.urls.to_numpy()
	num_tesis = df.num_thesis.to_numpy()

	n_total = len(num_tesis)

	data_find = pd.DataFrame()
	errors_df = pd.DataFrame()

	for i, url in enumerate(urls):
		percent = progress(i, n_total)
		# pri
		try:
			df = get_thesis_by_subitems(url, master_dirs[i], sub_dirs[i])
			data_find = pd.concat((data_find, df))
		except:
			df = {'dir': [master_dirs[i]], 'sub_dir': [sub_dirs[i]], 'url': [url]}
			df = pd.DataFrame(df)
			errors_less_20 = pd.concat((errors_df, df))
	return data_find, errors_df


def download_metadata_more20(df):
	master_dirs = df.master_dir.to_numpy()
	sub_dirs = df.dir_name.to_numpy()
	urls = df.urls.to_numpy()
	num_tesis = df.num_thesis.to_numpy()

	n_total = len(num_tesis)

	data_find = pd.DataFrame()
	errors_df = pd.DataFrame()

	for i, url in enumerate(urls):
		last_range = int(np.ceil(num_tesis[i] / 20))
		percent = progress(i, n_total)
		for page in range(last_range):
			page_url = url + f"/recent-submission?offset={page * 20}"
			try:
				df = get_thesis_by_subitems(page_url, master_dirs[i], sub_dirs[i])
				data_find = pd.concat((data_find, df))
			except:
				df = {'dir': [master_dirs[i]], 'sub_dir': [sub_dirs[i]], 'url': [url]}
				df = pd.DataFrame(df)
				errors_df = pd.concat((errors_df, df))
	return data_find, errors_df


	

