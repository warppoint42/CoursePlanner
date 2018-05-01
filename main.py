from selenium import webdriver
import time
import os

def performance_for(letter, data):
	start = letter + '","the_count":'
	end = '}'
	s = data
	return str(0.01 * float((s.split(start))[1].split(end)[0]))

def intensity_for(hrs, data):

	index = (data.find(hrs + " hrs"))
	if index == -1:
		return -1;
	
	index -= 25
	start = 'count":'
	end = ',"anchor"'
	s = data[index:];
	return str(0.01 * float((s.split(start))[1].split(end)[0]))

def get_intensity():
	
	l = str(intensity_for("\u003C 5", data))  + "," +\
	str(intensity_for("5 - 10", data)) + "," +\
	str(intensity_for("10 - 15", data)) + "," +\
	str(intensity_for("15 - 20", data)) + "," +\
	str(intensity_for("20 - 25", data)) + "," +\
	str(intensity_for("25 - 30", data)) + "," +\
	str(intensity_for("30 - 35", data)) + "," +\
	str(intensity_for("\u003E 35", data))
	return l

def get_performance():
	if(performance_for("A", data) == 0):
		# we can safely say that this course is C/NC, which we will ignore
		return -1;
	l = performance_for("A+", data) + "," +\
	performance_for("A", data) + "," +\
	performance_for("A-", data) + "," +\
	performance_for("B+", data) + "," +\
	performance_for("B", data) + "," +\
	performance_for("B-", data) + "," +\
	performance_for("C+", data) + "," +\
	performance_for("C", data) + "," +\
	performance_for("C-", data) + "," +\
	performance_for("D+", data) + "," +\
	performance_for("D", data) + "," +\
	performance_for("D-", data)
	return l

def calc_overall():
	if calc_intensity() != 0 and calc_performance() != -1:
		return calc_performance()/calc_intensity();
	return 0;

def course_exists(data):
	if data.find("Course not found!") != -1:
		return -1;
	return 1;

#########################################MAIN STARTS HERE


path_to_chromedriver = os.getcwd() + '/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'https://carta.stanford.edu/course/ECON52/'
browser.get(url) # UNCOMMENT IN FINAL VERSION

while "ECON52" not in browser.current_url:
	time.sleep(1)

# AUTHENTICATED

f = open('coursedata3', 'w');

with open("sources_extended2.csv", "r") as ins:
    #array = []
    for line in ins:
    	browser.get('https://carta.stanford.edu/course/'+line[0:line.find(",")])
    	data = browser.page_source
    	#if(calc_overall() != 0):
    	if course_exists(data) == 1:
    		print(line.strip() + "," + get_intensity() + "," + get_performance() + '\n')


# print(browser.page_source)


"""
with open('cartasample.html', 'r') as myfile:
    data=myfile.read().replace('\n', '')
"""







"""
while "ECON 52" not in browser.find_element_by_xpath(".//html").text:
	time.sleep(1)
	print(browser.find_element_by_xpath(".//html").text)


print("done loading");
html= browser.find_element_by_xpath(".//html")

print(html.text);
"""
