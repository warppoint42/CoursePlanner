from selenium import webdriver
import time
import os


# returns performance percentage for a letter as a string
def performance_for(letter, data):
    return str(percent_for(letter, data))


# returns performance percentage for a letter
def percent_for(letter, data):
    start = letter + '","the_count":'
    end = '}'
    s = data
    return 0.01 * float((s.split(start))[1].split(end)[0])


# returns intensity percentage for an hour range as a float
def intensity_for(hrs, data):
    index = (data.find(hrs + " hrs"))
    if index == -1:
        return 0
    index -= 25
    start = 'count":'
    end = ',"anchor"'
    s = data[index:]
    num = 0.01 * float((s.split(start))[1].split(end)[0])
    return num


# returns intensity data percentages
def get_intensity():
    l = str(intensity_for("\u003c 5", data)) + "," +\
    str(intensity_for("5 - 10", data)) + "," +\
    str(intensity_for("10 - 15", data)) + "," +\
    str(intensity_for("15 - 20", data)) + "," +\
    str(intensity_for("20 - 25", data)) + "," +\
    str(intensity_for("25 - 30", data)) + "," +\
    str(intensity_for("30 - 35", data)) + "," +\
    str(intensity_for("\u003e 35", data))
    return l


# makes a guess as to the average intensity for a course, 0 indicates no data
def get_avg_intensity():
    hrs = intensity_for("\u003c 5", data) * 2.5 + \
        intensity_for("5 - 10", data) * 7.5 +\
        intensity_for("10 - 15", data) * 12.5 +\
        intensity_for("15 - 20", data) * 17.5 +\
        intensity_for("20 - 25", data) * 22.5 +\
        intensity_for("25 - 30", data) * 27.5 +\
        intensity_for("30 - 35", data) * 32.5 +\
        intensity_for("\u003e 35", data) * 37.5
    return hrs


# returns grade distribution percentages
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


# returns the average gpa
def get_avg_gpa():
    if (performance_for("A", data) == 0):
        # we can safely say that this course is C/NC, which we will ignore
        return -1;
    # a value of 0 indicates no data
    gpa = percent_for("A+", data) * 4.3 + \
          percent_for("A", data) * 4.0 + \
          percent_for("A-", data) * 3.7 + \
          percent_for("B+", data) * 3.3 + \
          percent_for("B", data) * 3.0 + \
          percent_for("B-", data) * 2.7 + \
          percent_for("C+", data) * 2.3 + \
          percent_for("C", data) * 2.0 + \
          percent_for("C-", data) * 1.7 + \
          percent_for("D+", data) * 1.3 + \
          percent_for("D", data) * 1.0 + \
          percent_for("D-", data) * 0.7
    return gpa


# returns the terms a course is available, seperated by semicolons
def get_terms():
    index = data.find('Terms</strong><br />')
    if index == -1:
        return 'None'
    s = data[index:]
    start = '</strong><br />'
    end = '</div>'
    str = (s.split(start))[1].split(end)[0]
    seasons = []
    if "Autumn" in str:
        seasons.append("Autumn")
    if "Winter" in str:
        seasons.append("Winter")
    if "Spring" in str:
        seasons.append("Spring")
    if "Summer" in str:
        seasons.append("Summer")
    if len(seasons) == 0:
        return "None"
    return ';'.join(seasons)


# return the text in the Units feild
def get_units():
    index = data.find('Units</strong>')
    if index == -1:
        return 'N/A'
    s = data[index:]
    start = '<br />'
    end = '</div>'
    str = (s.split(start))[1].split(end)[0]
    return str.strip()


# return the text in the UG REQS field, replacing commas with semicolons
def get_UG_REQS():
    index = data.find('UG REQS</strong>')
    if index == -1:
        return 'N/A'
    s = data[index:]
    start = '<br />'
    end = '</div>'
    str = (s.split(start))[1].split(end)[0]
    return str.strip().replace(",", ";")


# returns course id, if it exists
def get_courseid():
    start = '"courseId":"'
    end = '",'
    s = data.split(start)
    s = s[len(s) - 1].split(end)[0]
    try:
        int(s)
        return s
    except ValueError:
        return ""


def calc_overall():
    if calc_intensity() != 0 and calc_performance() != -1:
        return calc_performance()/calc_intensity()
    return 0


# self-explanatory
def course_exists(data):
    if data.find("Course not found!") != -1:
        return -1
    return 1

#########################################MAIN STARTS HERE


path_to_chromedriver = os.getcwd() + '/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'https://carta.stanford.edu/course/ECON52/'
browser.get(url) # UNCOMMENT IN FINAL VERSION

while "ECON52" not in browser.current_url:
    time.sleep(1)

# AUTHENTICATED

f = open('coursedata3.csv', 'w')
f.truncate() #Erases the file, comment to disable

with open("sources_cleaned.csv", "r") as ins:
    for line in ins:
        browser.get('https://carta.stanford.edu/course/'+line[0:line.find(",")])
        data = browser.page_source
        if course_exists(data) == 1:
            id = get_courseid()
            # enable to filter out courses without ids
            # if id != "":
            # format: id,shortname,name,school,dept,grading,reqs,terms,gpa,hrs
            f.write(id + ',' + line.strip() + ',' + get_UG_REQS() + ',' + get_terms() + ','
                    + str(get_avg_gpa()) + ',' + str(get_avg_intensity()) + '\n')


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
