import csv
import hashlib
from collections import Counter
import statistics
import numpy as np
from functools import reduce
import plotly.express as px
import plotly.io as pio
import pandas as pd
from itertools import product

colors = ["#636EFA", "#32DC43", "#FB0D0D", "#332288", "#E4DA21", "#C41899"]
pio.templates["plotly"].layout.colorway = colors

responses = []
with open("SurveyValid.csv", "r") as file:
    reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
    # ROWS:
    #    0 = Column Names
    #    1 = Column Descriptions
    #    2 = Column Type
    #   3+ = Answers
    # COLUMNS:
    #    0 = StartDate
    #    1 = EndDate
    #    2 = Status
    #    3 = Progress
    #    4 = Duration (seconds)
    #    5 = Finished
    #    6 = RecordedDate
    #    7 = ResponseId
    #    8 = DistributionChannel
    #    9 = UserLanguage
    #   Q1 = Which features are allowed on The Server?
    #   10 = Q1_1 Markdown Headers
    #   11 = Q1_2 Markdown Footers
    #   12 = Q1_3 Markdown Masked Links
    #   13 = Q1_4 Bold/Italic/Underlined 
    #   14 = Q1_5 Non-Standard Fonts
    #   15 = Q1_6 Changing Nickname
    #   16 = Q1_7 Forwarded Messages
    #   17 = Q1_8 External Applications
    #   18 = Q1_9 Custom Emojis
    #   19 = Q1_10 Default Emojis
    #   20 = Q1_11 Server Invites
    #   Q2 = How often do Features get used?
    #   21 = Q2_1 Markdown Headers
    #   22 = Q2_2 Markdown Footers
    #   23 = Q2_3 Markdown Masked Links
    #   24 = Q2_4 Bold/Italic/Underline
    #   25 = Q2_5 Non-Standard Fonts
    #   26 = Q2_6 Changing Nickname
    #   27 = Q2_7 Forwarded Messages
    #   28 = Q2_8 External Applications
    #   29 = Q2_9 Custom Emojis
    #   30 = Q2_10 Default Emojis
    #   31 = Q2_11 Server Invites
    #   Q3 = Which features have been used for Problematic Messages?
    #   32 = Q3 All options from above, comma separated
    #   Q4 = How prevalent is content of Problematic Messages?
    #   33 = Q4_1 NSFW
    #   34 = Q4_2 Gifts
    #   35 = Q4_3 Crypto
    #   36 = Q4_4 Digital Currencies
    #   37 = Q4_5 Supposed Doxxing
    #   38 = Q4_6 Redirecting to DMs
    #   Q5 = Which systems does the server utilize?
    #   39 = Q5 Default Automod Protection, Custom Automod Rules, Public Custom Bot, Self-written, Highest Verification Level, Logging
    #   Q6 = How often do Problematic Messages get posted?
    #   40 = Q6 Hourly/Daily/Multiple times per week/Multiple times per month/Once per month, or less often/NA
    #   Q7 = Which systems catch the most Problematic Messages
    #   41 = Q7_1 Default Automod Protection
    #   42 = Q7_2 Custom Automod Rules
    #   43 = Q7_3 Public Custom Bot
    #   44 = Q7_4 Self-written Custom Bot
    #   Q8 = How often do Problematic Messages *not* get caught?
    #   45 = Q8 Hourly/Daily/Multiple times per week/Multiple times per month/Once per month, or less often/No Problematic Message has gotten through
    #   Q9 = How long does it take to get removed manually?
    #   46 = Q9 Less than a minute/A few minutes/Up to an hour/Multiple hours/More than 12 hours
    #  Q10 = Which labels best represent the server?
    #   47 = Q10 Gaming/Music, Art Writing/Other Entertainment Media/Based around Content Creators/NSFW/Science, Tech, Dev, Programming/Sport, Fitness, Health/Finance, Investing/Education/Based around a local group/Community/Other
    #  Q11 = How is the server accessible?
    #   48 = Q11 Public invite, discovery, everyone can create invites, only some can create invites, staff invites
    #  Q12 = How many members are on the server?
    #   49 = Q12 free input number
    #  Q13 = What is the server ID?
    #   50 = Q13 free input number
    for row in reader:
        response = {}

        # StartDate, EndDate, Status, Progress, Duration (seconds), Finished, RecordedDate, ResponseId, DistributionChannel, UserLanguage
        response["metadata"] = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]
        # "Not allowed", "Locked behind a role", "Allowed"
        response["q1"] = [row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20]]
        # "Never heard of it before", "Never seen it used", "Seen it used rarely", "See it used regularly"
        response["q2"] = [row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31]]
        # "Markdown Headers", "Markdown Footers (subtext)", "Markdown Masked Links", "Bold/Italic/Underline Text", "Changed Nickname", "Forwarded Messages", "External Applications", "Custom Emojis (from other servers)", "Default Emojis", "Server Invites"
        response["q3"] = [row[32]]
        # 1,2,3,4,5,6 in order NSFW, Gifts, Crypto, other currencies, Doxxing, Redirecting
        response["q4"] = [row[33], row[34], row[35], row[36], row[37], row[38]]
        # "Default Automod Protection", "Custom Automod Rules", "Public Custom Bot (i.e. Dyno, Hashbot)", "Self-written (or augmented and self hosted) Custom Bot", "Highest Verification Level (Accounts must have a verified phonE)", "Logging of (automatically) removed messages"
        response["q5"] = [row[39]]
        # "Hourly", "Daily", "Multiple times per week", "Multiple times per month", "Once per month, or less often", "N/A"
        response["q6"] = [row[40]]
        # 1,2,3,4 in order Default Automod Protection, Custom Automod Rules, Public Custom Bot, Self-written Custom Bot
        response["q7"] = [row[41], row[42], row[43], row[44]]
        # "Hourly", "Daily", "Multiple times per week", "Multiple times per month", "Once per month, or less often", "No Problematic Message has gotten through"
        response["q8"] = [row[45]]
        # "Less than a minute (i.e. there is always a Moderator available)", "A few minutes", "Up to an hour", "Multiple hours", "More than 12 hours"
        response["q9"] = [row[46]]
        # "Gaming (incl. Tabletop Games)", "Music, Art, Writing, and further creative pursuits", "Other Entertainment Media (Movies, Shows, Books, Comics, etc)", "Based around one (or a group of) Content Creator(s) (Incld. Podcasts)", "NSFW Adult Content", "Science, Tech, Development and Programming", "Sport, Fitness and Health", "Finance, Investing, and other money related topics", "Education", "Based around a local group which does not, or only partially, fit in the above categories", "Community", "Other"
        response["q10"] = [row[47]]
        # "Public invite through a website, subreddit, video description, etc", "Server Discovery", "all server members can create invites", "Only certain server members can create invites (i.e. if level locked)", "Staff members can create invites"
        response["q11"] = [row[48]]
        # free field number entry (amount of server members)
        response["q12"] = [row[49]]
        # free field number entry (Server ID)
        response["q13"] = [hashlib.sha256(bytes(row[50], 'utf-8')).hexdigest()]

        responses.append(response)
responses = responses[3:] # remove metadata rows


def same_server():
    # creates a dict with server IDs as key to group same server responses
    known = dict()
    for response in responses:
        if response["q13"][0] not in known.keys():
            known[response["q13"][0]] = [response]
        else:
            known[response["q13"][0]].append(response)
    return known


def condense(responses):
    condensed = {}
    # Q1:
    q1_list = []
    for i in range(11):
        answers = extract_answers(responses, "q1", i)
        q1_list.append(Counter(answers).most_common(1)[0][0])
    condensed["q1"] = q1_list
    # Q2:
    q2_list = []
    for i in range(11):
        answers = extract_answers(responses, "q2", i)
        if not answers:
            q2_list.append("")
            continue
        q2_list.append(Counter(answers).most_common(1)[0][0])
    condensed["q2"] = q2_list
    # Q3:
    answers = []
    for r in responses:
        answers.append(r["q3"])
    condensed["q3"] = reduce(np.intersect1d, answers)
    # Q4:
    q4_list = []
    for i in range(6):
        answers = extract_answers(responses, "q4", i)
        q4_list.append(Counter(answers).most_common(1)[0][0])
        # alternatively:
        # q4_list.append(statistics.median(answers))
    condensed["q4"] = q4_list
    # Q5:
    answers = []
    for r in responses:
        answers.append(r["q5"])
    condensed["q5"] = reduce(np.intersect1d, answers)
    # Q6:
    answers = []
    for r in responses:
        a = r["q6"][0]
        if a == "":
            continue
        answers.append(a)
    condensed["q6"] = Counter(answers).most_common(1)[0][0]
    # alternatively:
    # condensed["q6"] = q6_compare(statistics.median(answers), True)
    # Q7:
    q7_list = []
    for i in range(4):
        answers = extract_answers(responses, "q7", i)
        answers = list(map(int, answers))
        q7_list.append(Counter(answers).most_common(1)[0][0])
        # alternatively:
        # if len(answers) % 2 == 0:
        #     answers.append(0) # alternatively answers.append(5)
        # q7_list.append(statistics.median(answers))
    condensed["q7"] = q7_list
    # Q8:
    answers = []
    for r in responses:
        answers.append(q8_compare(r["q8"][0]))
    condensed["q8"] = Counter(answers).most_common(1)[0][0]
    # alternatively:
    # condensed["q8"] = q8_compare(statistics.median(answers), True)
    # Q9:
    answers = []
    for r in responses:
        a = r["q9"][0]
        if a != "":
            answers.append(q9_compare(a))
    condensed["q9"] = Counter(answers).most_common(1)[0][0]
    # alternatively:
    # condensed["q9"] = q9_compare(statistics.median(answers), True)
    # Q10:
    answers = []
    for r in responses:
        answers.append(r["q10"])
    condensed["q10"] = reduce(np.intersect1d, answers)
    # Q11:
    answers = []
    for r in responses:
        answers.append(r["q11"])
    condensed["q11"] = reduce(np.intersect1d, answers)
    # Q12:
    answers = []
    for r in responses:
        a = r["q12"][0]
        if a != "":
            answers.append(int(a))
    condensed["q12"] = int(statistics.fmean(answers))
    # Q13:
    condensed["q13"] = responses[0]["q13"]

    return condensed


def extract_answers(responses, question, index):
    answers = []
    for r in responses:
        try:
            a = r[question][index]
        except:
            continue
        if a != "":
            answers.append(a)
    return answers


def q6_compare(s, rev=False):
    if rev:
        compdict = {}
        compdict[0] = "N/A"
        compdict[1] = "Once per month, or less often"
        compdict[2] = "Multiple times per month"
        compdict[3] = "Multiple times per week"
        compdict[4] = "Daily"
        compdict[5] = "Hourly"
        return compdict[s]
    compdict = {}
    compdict["N/A"] = 0
    compdict["Once per month, or less often"] = 1
    compdict["Multiple times per month"] = 2
    compdict["Multiple times per week"] = 3
    compdict["Daily"] = 4
    compdict["Hourly"] = 5
    return compdict[s]


def q8_compare(s, rev=False):
    if rev:
        compdict = {}
        compdict[0] = "No Problematic Message has gotten through"
        compdict[1] = "Once per month, or less often"
        compdict[2] = "Multiple times per month"
        compdict[3] = "Multiple times per week"
        compdict[4] = "Daily"
        compdict[5] = "Hourly"
        return compdict[s]
    compdict = {}
    compdict["No Problematic Message has gotten through"] = 0
    compdict["Once per month, or less often"] = 1
    compdict["Multiple times per month"] = 2
    compdict["Multiple times per week"] = 3
    compdict["Daily"] = 4
    compdict["Hourly"] = 5
    return compdict[s]


def q9_compare(s, rev=False):
    if rev:
        compdict = {}
        compdict[0] = "More than 12 hours"
        compdict[1] = "Multiple hours"
        compdict[2] = "Up to an hour"
        compdict[3] = "A few minutes"
        compdict[4] = "Less than a minute (i.e. there is always a Moderator available)"
        return compdict[s]
    compdict = {}
    compdict["More than 12 hours"] = 0
    compdict["Multiple hours"] = 1
    compdict["Up to an hour"] = 2
    compdict["A few minutes"] = 3
    compdict["Less than a minute (i.e. there is always a Moderator available)"] = 4
    return compdict[s]


def fix_data():
    for r in responses:
        answer = r["q7"]
        nrs = []
        for v in answer:
            if v:
                nrs.append(int(v))
        for i, v in enumerate(answer):
            if not v:
                r["q7"][i] = "0"


def q1_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q1"])

    numbered = {}
    for answer in answers:
        for i, a in enumerate(answer):
            if i not in numbered.keys():
                numbered[i] = [a]
            else:
                numbered[i].append(a)

    answer_amounts = []
    for i in range(11):
        answer_amounts.append(Counter(numbered[i]).most_common())
    for a in answer_amounts:
        if len(a) == 3:
            continue
        a.append(('Locked behind a role', 0))
        
    features = ["Markdown Headers", "Markdown Footers", "Markdown Masked Links", "Bold/Italic/Underline Text", "Non-Standard Fonts", "Changed Nicknames", "Forwarded Messages", "External Applications", "Custom Emojis", "Default Emojis", "Server Invites"]
    perms = ["Allowed", "Restricted", "Prohibited"]
    amounts = [5,2,3, 7,1,2, 5,3,2, 9,0,1, 5,1,4, 7,2,1, 8,0,2, 2,0,8, 6,3,1, 9,0,1, 3,1,6] 
    # this could be done automatically by extracting from answer_amounts but requires extra work due to data extraction inconsistencies

    d = pd.DataFrame(product(features, perms), columns=["Feature", "Permission"])
    d["Amount"] = amounts

    fig = px.bar(d, x="Feature", y="Amount", color="Permission")
    fig.update_layout(
        xaxis_title=dict(text="Message Feature", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q2_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q2"])

    numbered = {}
    for answer in answers:
        for i, a in enumerate(answer):
            if i not in numbered.keys():
                numbered[i] = [a]
            else:
                numbered[i].append(a)

    answer_amounts = []
    for i in range(11):
        answer_amounts.append(Counter(numbered[i]).most_common())

    features = ["Markdown Headers", "Markdown Footers", "Markdown Masked Links", "Bold/Italic/Underline Text", "Non-Standard Fonts", "Changed Nicknames", "Forwarded Messages", "External Applications", "Custom Emojis", "Default Emojis", "Server Invites"]
    used = ["Never", "Rarely", "Regularly"]
    amounts = [3,2,2, 3,4,1, 2,3,3, 0,2,7, 2,3,1, 0,0,9, 1,3,4, 0,1,1, 0,1,8, 0,0,9, 0,1,3] 
    # this could be done automatically by extracting from answer_amounts but requires extra work due to data extraction inconsistencies

    d = pd.DataFrame(product(features, used), columns=["Feature", "Usage"])
    d["Amount"] = amounts

    fig = px.bar(d, x="Feature", y="Amount", color="Usage")
    fig.update_layout(
        xaxis_title=dict(text="Message Feature", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q3_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q3"])
    full_answers = []
    for ans in answers:
        an = ans[0].split(',')
        for a in an:
            full_answers.append(a)

    answer_amounts = Counter(full_answers).most_common()

    features = []
    amounts = []
    for f, a in answer_amounts:
        features.append(f)
        amounts.append(a)
    
    d = pd.DataFrame({"Feature": features, "Amount": amounts})
    fig = px.bar(d, x="Feature", y="Amount")
    fig.update_layout(
        xaxis_title=dict(text="Message Feature", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q4_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q4"])
    flattened_answers = [a for ans in answers for a in ans]

    contents = ["NSFW", "Gifts", "Crypto", "Other Currencies", "Doxxing", "Redirection"]
    d = pd.DataFrame(contents*len(final_responses), columns=["content"])
    d["ratings"] = flattened_answers

    fig = px.histogram(d, x="content", color="ratings", histfunc='sum',
                category_orders={"content": ["NSFW", "Gifts", "Crypto", "Other Currencies", "Doxxing", "Redirection"], 
                                "ratings": ["1","2","3","4","5","6"]})
    fig.update_layout(legend_title="Occurrence from most(1) to least(6) often")
    fig.update_layout(
        xaxis_title=dict(text="Message Content", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q5_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q5"])
    full_answers_ext = []
    for ans in answers:
        an = ans[0].split(',')
        for a in an:
            full_answers_ext.append(a)

    full_answers = []
    for answer in full_answers_ext:
        if answer.startswith("Public Custom Bot"):
            full_answers.append("Public Custom Bot")
        elif answer.startswith("Self-written"):
            full_answers.append("Self-written/hosted Custom Bot")
        elif answer.startswith("Highest Verification"):
            full_answers.append("Highest Verification Level")
        elif answer.startswith("Logging"):
            full_answers.append("Logging")
        elif answer == " Hashbot)":
            # this happens because I split at commas and cba to fix the root cause
            continue
        else:
            full_answers.append(answer)

    answer_amounts = Counter(full_answers).most_common()

    features = []
    amounts = []
    for f, a in answer_amounts:
        features.append(f)
        amounts.append(a)
    
    d = pd.DataFrame({"Tool": features, "Amount": amounts})
    fig = px.bar(d, x="Tool", y="Amount")
    fig.update_layout(
        xaxis_title=dict(text="Tool", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q6_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q6"])
    flattened_answers = [a for ans in answers for a in ans]

    answer_counts = Counter(flattened_answers).most_common()
    answer_counts.append(('Once per month or less', 0))
    
    frequency = []
    amounts = []
    for f, a in answer_counts:
        frequency.append(f)
        amounts.append(a)
    
    d = pd.DataFrame({"Frequency": frequency, "Count": amounts})
    fig = px.bar(d, x="Frequency", y="Count", category_orders={"Frequency": ["Hourly", "Daily", "Multiple times per week", "Multiple times per month", "Once per month or less"]})
    fig.update_layout(
        xaxis_title=dict(text="Frequency of spam", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q7_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q7"])
    flattened_answers = [a for ans in answers for a in ans]
    

    systems = ["Default Automod Protection", "Custom Automod Rules", "Public Custom Bot", "Self-written Custom Bot"]
    d = pd.DataFrame(systems*len(final_responses), columns=["system"])
    d["ratings"] = flattened_answers

    fig = px.histogram(d, x="system", color="ratings", histfunc='sum',
                category_orders={"system": ["Default Automod Protection", "Custom Automod Rules", "Public Custom Bot", "Self-written Custom Bot"], 
                                "ratings": ["1","2","3","4","0"]})
    fig.update_layout(legend_title="Performance from best(1) to worst(4)")
    fig.update_layout(
        xaxis_title=dict(text="Moderation Tool", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()
    

def q8_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q8"])
    flattened_answers = [a for ans in answers for a in ans]

    answer_counts = Counter(flattened_answers).most_common()
    answer_counts.append(('Hourly', 0))
    
    frequency = []
    amounts = []
    for f, a in answer_counts:
        frequency.append(f)
        amounts.append(a)
    
    d = pd.DataFrame({"Frequency": frequency, "Count": amounts})
    fig = px.bar(d, x="Frequency", y="Count", category_orders={"Frequency": ["Hourly", "Daily", "Multiple times per week", "Multiple times per month", "Once per month, or less often"]})
    fig.update_layout(
        xaxis_title=dict(text="Frequency of spam bypassing filters", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q9_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q9"])
    flattened_answers = [a for ans in answers for a in ans]

    answer_counts = Counter(flattened_answers).most_common()
    answer_counts.append(('Multiple hours', 0))
    answer_counts.remove(('', 1))
    answer_counts.remove(('Less than a minute (i.e. there is always a Moderator available)', 1))
    answer_counts.append(('Less than a minute', 1))
    
    duration = []
    amounts = []
    for f, a in answer_counts:
        duration.append(f)
        amounts.append(a)
    
    d = pd.DataFrame({"Duration": duration, "Count": amounts})
    fig = px.bar(d, x="Duration", y="Count", category_orders={"Duration": ["Less than a minute", "A few minutes", "Up to an hour", "Multiple hours"]})
    fig.update_layout(
        xaxis_title=dict(text="Time until human Moderator intervention", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q10_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q10"])
    full_answers_ext = []
    for ans in answers:
        an = ans[0].split(',')
        for a in an:
            full_answers_ext.append(a)

    full_answers = []
    for answer in full_answers_ext:
        if answer.startswith("Music"):
            full_answers.append("Music, Art, Writing, and further creative pursuits")
        elif answer.startswith("Other Entertainment"):
            full_answers.append("Other Entertainment Media")
        elif answer.startswith("Based around one"):
            full_answers.append("Based around Content Creators")
        elif answer.startswith("Science"):
            full_answers.append("Science, Tech, Development and Programming")
        elif answer.startswith("Sport"):
            full_answers.append("Sport, Fitness and Health")
        elif answer.startswith("Finance"):
            full_answers.append("Finance, Investing, and other money related topics")
        elif answer.startswith("Based around a local group"):
            full_answers.append("Based around a local group")
        elif answer == " Art" or answer == " Writing" or answer == " and further creative pursuits" or answer == " Shows" or answer == " Books" or answer == " Comics" or answer == " etc)" or answer == " Tech" or answer == " Development and Programming" or answer == " Fitness and Health" or answer == " Investing" or answer == " and other money related topics" or answer == " or only partially" or answer == " fit in the above categories":
            # this happens because I split at commas and cba to fix the root cause
            continue
        else:
            full_answers.append(answer)

    answer_amounts = Counter(full_answers).most_common()

    labels = []
    amounts = []
    for f, a in answer_amounts:
        labels.append(f)
        amounts.append(a)
    
    d = pd.DataFrame({"Label": labels, "Amount": amounts})
    fig = px.bar(d, x="Label", y="Amount")
    fig.update_layout(
        xaxis_title=dict(text="Server Label", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q11_fix(answers):
    full_answers_ext = []
    for ans in answers:
        an = ans[0].split(',')
        for a in an:
            full_answers_ext.append(a)

    full_answers = []
    for answer in full_answers_ext:
        if answer.startswith("Public invite"):
            full_answers.append("Public invite through a website, subreddit, etc")
        elif answer.startswith("Only certain"):
            full_answers.append("Only certain server members can create invites")
        elif answer == " subreddit" or answer == " video description" or answer == " etc":
            # this happens because I split at commas and cba to fix the root cause
            continue
        else:
            full_answers.append(answer)
    return full_answers


def q11_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q11"])

    full_answers = q11_fix(answers)

    answer_amounts = Counter(full_answers).most_common()

    access = []
    amounts = []
    for f, a in answer_amounts:
        access.append(f)
        amounts.append(a)
    
    d = pd.DataFrame({"Access": access, "Amount": amounts})
    fig = px.bar(d, x="Access", y="Amount")
    fig.update_layout(
        xaxis_title=dict(text="Type of access to the server", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def q12_barchart():
    answers = []
    for response in final_responses:
        answers.append(response["q12"])
    answers_flat = [int(x) for ans in answers for x in ans]
    bins = pd.IntervalIndex([pd.Interval(0, 999), pd.Interval(1000, 9999), pd.Interval(10000, 99999), pd.Interval(100000, 999999)])
    buckets = pd.cut(answers_flat, bins=bins)
    
    bucket_strings = []
    for interval in buckets:
        if interval.left == 0:
            bucket_strings.append("0 - 1,000")
        elif interval.left == 1000:
            bucket_strings.append("1,000 - 10,000")
        elif interval.left == 10000:
            bucket_strings.append("10,000 - 100,000")
        else:
            bucket_strings.append("100,000 +")
    
    d = pd.DataFrame({"Buckets": bucket_strings})
    fig = px.histogram(d, x="Buckets", histfunc="sum", category_orders={"Buckets": ["0 - 1,000", "1,000 - 10,000", "10,000 - 100,000", "100,000 +"]})
    fig.update_layout(
        xaxis_title=dict(text="Member Count", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )

    fig.show()


def bot_comp(tools, bucket_strings):
    bots = []
    for answer in tools:
        if "Public Custom Bot" in answer[0]:
            if "Self-written" in answer[0]:
                bots.append("Both")
            else:
                bots.append("Public")
        elif "Self-written" in answer[0]:
            bots.append("Self-written")
        else:
            bots.append("Neither")

    d = pd.DataFrame({"Buckets": bucket_strings, "Bots": bots})
    d_counts = d.groupby(["Buckets", "Bots"]).size().reset_index(name="count")
    d_counts["percentage"] = d_counts.groupby("Buckets")["count"].transform(lambda x: (100*x/x.sum())/100)

    fig = px.bar(d_counts, x="Buckets", y="percentage", color="Bots", category_orders={"Buckets": ["0 - 1,000", "1,000 - 10,000", "10,000 - 100,000", "100,000 +"], "Bots": ["Public", "Self-written", "Both"]})
    fig.update_layout(
        xaxis_title=dict(text="Server Size", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text=r"Nr of servers in % of bucket population", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.layout.yaxis.tickformat = '.0%'
    fig.show()


def auto_comp(tools, bucket_strings):
    automod = []
    for answer in tools:
        if "Default Automod" in answer[0]:
            if "Custom Automod" in answer[0]:
                automod.append("Both")
            else:
                automod.append("Default")
        elif "Custom Automod" in answer[0]:
            automod.append("Customized")
        else:
            automod.append("Neither")
            
    d = pd.DataFrame({"Buckets": bucket_strings, "Automod": automod})
    d_counts = d.groupby(["Buckets", "Automod"]).size().reset_index(name="count")
    d_counts["percentage"] = d_counts.groupby("Buckets")["count"].transform(lambda x: (100*x/x.sum())/100)

    fig = px.bar(d_counts, x="Buckets", y="percentage", color="Automod", category_orders={"Buckets": ["0 - 1,000", "1,000 - 10,000", "10,000 - 100,000", "100,000 +"], "Automod": ["Default", "Customized", "Both", "Neither"]})
    fig.update_layout(
        xaxis_title=dict(text="Server Size", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text=r"Nr of servers in % of bucket population", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.layout.yaxis.tickformat = '.0%'
    fig.show()


def freq_comp(frequency, bucket_strings):
    frequency = [a for ans in frequency for a in ans]
    
    d = pd.DataFrame({"Buckets": bucket_strings, "Frequency": frequency})
    d_counts = d.groupby(["Buckets", "Frequency"]).size().reset_index(name="count")
    d_counts["percentage"] = d_counts.groupby("Buckets")["count"].transform(lambda x: (100*x/x.sum())/100)

    fig = px.bar(d_counts, x="Buckets", y="percentage", color="Frequency", category_orders={"Buckets": ["0 - 1,000", "1,000 - 10,000", "10,000 - 100,000", "100,000 +"], "Frequency": ["Hourly", "Daily", "Multiple times per week", "Multiple times per month"]})
    fig.update_layout(
        xaxis_title=dict(text="Server Size", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text=r"Nr of servers in % of bucket population", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.layout.yaxis.tickformat = '.0%'
    fig.show()


def cont_comp(content, bucket_strings):
    topics = ["NSFW", "Gifts", "Crypto", "Other Currencies", "Doxxing", "Redirection"]
    nr_1 = []
    for ratings in content:
        nr_1.append(topics[ratings.index("1")])

    d = pd.DataFrame({"Buckets": bucket_strings, "Nr1": nr_1})
    d_counts = d.groupby(["Buckets", "Nr1"]).size().reset_index(name="count")
    d_counts["percentage"] = d_counts.groupby("Buckets")["count"].transform(lambda x: (100*x/x.sum())/100)

    fig = px.bar(d_counts, x="Buckets", y="percentage", color="Nr1", category_orders={"Buckets": ["0 - 1,000", "1,000 - 10,000", "10,000 - 100,000", "100,000 +"]})
    fig.update_layout(
        xaxis_title=dict(text="Server Size", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text=r"Nr of servers in % of bucket population", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.layout.yaxis.tickformat = '.0%'
    fig.show()


def cont_comp2(content, bucket_strings):
    topics = ["NSFW", "Gifts", "Crypto", "Other Currencies", "Doxxing", "Redirection"]
    nr_1 = []
    nr_2 = []
    nr_3 = []
    for ratings in content:
        nr_1.append(topics[ratings.index("1")])
        nr_2.append(topics[ratings.index("2")])
        nr_3.append(topics[ratings.index("3")])
    
    sets = {"NSFW": set(), "Gifts": set(), "Crypto": set(), "Other Currencies": set(), "Doxxing": set(), "Redirection": set()}
    for i, t in enumerate(nr_1):
        sets[t].add(bucket_strings[i])
    for i, t in enumerate(nr_2):
        sets[t].add(bucket_strings[i])
    for i, t in enumerate(nr_3):
        sets[t].add(bucket_strings[i])
    
    servers = []
    for topic in topics:
        servers.append(list(sets[topic]))
    
    buckets = ['0 - 1,000', '1,000 - 10,000', '10,000 - 100,000', '100,000 +']
    bucket_0 = []
    bucket_1 = []
    bucket_2 = []
    bucket_3 = []
    for i, bucket in enumerate(buckets):
        for top in servers:
            if bucket in top:
                if i == 0: bucket_0.append(1)
                if i == 1: bucket_1.append(1)
                if i == 2: bucket_2.append(1)
                if i == 3: bucket_3.append(1)
            else:
                if i == 0: bucket_0.append(0)
                if i == 1: bucket_1.append(0)
                if i == 2: bucket_2.append(0)
                if i == 3: bucket_3.append(0)

    d = pd.DataFrame({"Topics": topics, '0 - 1,000': bucket_0, '1,000 - 10,000': bucket_1, '10,000 - 100,000': bucket_2, '100,000 +': bucket_3})
    d = d.melt(id_vars=["Topics"], var_name="Bucket", value_name="Count")
    fig = px.bar(d, x = "Topics", y = "Count", color="Bucket", barmode="stack")
    fig.update_layout(
        xaxis_title=dict(text="Server Size", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text=r"Nr of servers in % of bucket population", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()

def speed_comp(speed, bucket_strings):
    # removes empty data irellevant for this plot
    del speed[2] 
    del bucket_strings[2]

    duration = []

    for answer in speed:
        answer = answer[0]
        if "Less" in answer:
            duration.append("Less than a minute")
        elif "A few" in answer:
            duration.append("A few minutes")
        elif "Up to" in answer:
            duration.append("Up to an hour")
        elif "Multiple" in answer:
            duration.append("Multiple hours")
        else:
            duration.append("More than 12 hours")

    d = pd.DataFrame({"Buckets": bucket_strings, "Duration": duration})
    d_counts = d.groupby(["Buckets", "Duration"]).size().reset_index(name="count")
    d_counts["percentage"] = d_counts.groupby("Buckets")["count"].transform(lambda x: (100*x/x.sum())/100)

    fig = px.bar(d_counts, x="Buckets", y="percentage", color="Duration", category_orders={"Buckets": ["0 - 1,000", "1,000 - 10,000", "10,000 - 100,000", "100,000 +"], "Duration": ["Less than a minute", "A few minutes", "Up to an hour", "Multiple hours", "More than 12 hours"]})
    fig.update_layout(
        xaxis_title=dict(text="Server Size", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text=r"Nr of servers in % of bucket population", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.layout.yaxis.tickformat = '.0%'
    fig.show()


def sizecomp(bot, auto, freq, cont, speed):
    sizes = [] # Q12
    tools = [] # Q5
    permissions = [] #Q1
    content = [] # Q4
    frequency = [] # Q6
    speed = [] #Q9
    for response in final_responses:
        sizes.append(response["q12"])
        tools.append(response["q5"])
        permissions.append(response["q1"])
        content.append(response["q4"])
        frequency.append(response["q6"])
        speed.append(response["q9"])

    # ----------------------
    # Creating Buckets
    sizes_flat = [int(x) for ans in sizes for x in ans]
    bins = pd.IntervalIndex([pd.Interval(0, 999), pd.Interval(1000, 9999), pd.Interval(10000, 99999), pd.Interval(100000, 999999)])
    buckets = pd.cut(sizes_flat, bins=bins)
    
    bucket_strings = []
    for interval in buckets:
        if interval.left == 0:
            bucket_strings.append("0 - 1,000")
        elif interval.left == 1000:
            bucket_strings.append("1,000 - 10,000")
        elif interval.left == 10000:
            bucket_strings.append("10,000 - 100,000")
        else:
            bucket_strings.append("100,000 +")
    # ----------------------

    if bot:
        bot_comp(tools, bucket_strings)

    if auto:
        auto_comp(tools, bucket_strings)

    if freq:
        freq_comp(frequency, bucket_strings)

    if cont:
        cont_comp(content, bucket_strings)
        cont_comp2(content, bucket_strings)

    if speed:
        speed_comp(speed, bucket_strings)


def accessamountcomp():
    amounts = [] #Q6
    access_tmp = [] #Q11
    for response in final_responses:
        amounts.append(response["q6"][0])
        access_tmp.append(response["q11"])

    # This is mostly just q11_fix() but I need the list to not be flattened
    access = []
    for answ in access_tmp:
        access_ext = []
        an = answ[0].split(',')
        for a in an:
            access_ext.append(a)
        
        full_answer = []
        for answer in access_ext:
            if answer.startswith("Public invite"):
                full_answer.append("Public invite")
            elif answer.startswith("Only certain"):
                full_answer.append("Restricted permission to create invites")
            elif answer == " subreddit" or answer == " video description" or answer == " etc":
                continue
            else:
                full_answer.append(answer)
        access.append(full_answer)
    
    data = []
    for i, am in enumerate(amounts):
        inp = []
        inp.append(am)
        cur_ac = access[i]
        if "Public invite" in cur_ac:
            inp.append(1)
            inp.append(0)
            inp.append(0)
            inp.append(0)
        else:
            inp.append(0)
            if "Server Discovery" in cur_ac:
                inp.append(1)
                inp.append(0)
                inp.append(0)
            else:
                inp.append(0)
                if "All server members can create invites" in cur_ac:
                    inp.append(1)
                    inp.append(0)
                else:
                    inp.append(0)
                    if "Staff members can create invites" in cur_ac:
                        inp.append(1)
                    else:
                        inp.append(0)
        data.append(inp)

    d = pd.DataFrame(data=data, columns=["Amount", "Public invite", "Server Discovery", "Free invite creation", "Restricted invite creation"])
    fig = px.histogram(d, x="Amount", y=["Public invite", "Server Discovery", "Free invite creation", "Restricted invite creation"], histfunc="sum",
                       category_orders={"Amount": ["Hourly", "Daily", "Multiple times per week", "Multiple times per month"]})
    fig.update_layout(legend_title="Type of access")
    fig.update_layout(
        xaxis_title=dict(text="Frequency of Spam", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def effectiveness_fail():
    automod = []
    custom = []
    for response in final_responses:
        answer = response["q5"]
        mod = False
        bot = False
        an = answer[0].split(',')
        for a in an:
            if not bot and (a.startswith("Public Custom Bot") or a.startswith("Self-written")):
                bot = True
                custom.append(1)
            elif not mod and (a.startswith("Custom Automod") or a.startswith("Default Automod")):
                mod = True
                automod.append(1)
            else:
                continue 
        if not mod:
            automod.append(0)
        if not bot:
            custom.append(0)

    freq = []
    for response in final_responses:
        freq.append(response["q8"])
    frequency = []
    for f in freq:
        frequency.append(f[0])

    d = pd.DataFrame({"Frequency": frequency, "Automod": automod, "Custom Bot": custom})
    d = d.melt(id_vars=["Frequency"], var_name="Tools", value_name="Count")
    fig = px.histogram(d, x="Frequency", y="Count", color="Tools", histfunc="sum", category_orders={"Frequency": ["Daily", "Multiple times per week", "Once per month, or less often", "Multiple times per month", "No Problematic Message has gotten through"]})
    fig.update_layout(
        xaxis_title=dict(text="Frequency of Spam", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def effectiveness_prevent():
    automod = []
    custom = []
    verification = []
    for response in final_responses:
        answer = response["q5"]
        mod = False
        bot = False
        ver = False
        an = answer[0].split(',')
        for a in an:
            if not bot and (a.startswith("Public Custom Bot") or a.startswith("Self-written")):
                bot = True
                custom.append(1)
            elif a.startswith("Highest Verification"):
                ver = True
                verification.append(1)
            elif not mod and (a.startswith("Custom Automod") or a.startswith("Default Automod")):
                mod = True
                automod.append(1)
            else:
                continue 
        if not mod:
            automod.append(0)
        if not bot:
            custom.append(0)
        if not ver:
            verification.append(0)

    freq = []
    for response in final_responses:
        freq.append(response["q6"])
    frequency = []
    for f in freq:
        frequency.append(f[0])

    d = pd.DataFrame({"Frequency": frequency, "Automod": automod, "Custom Bot": custom, "Highest Verification": verification})
    d = d.melt(id_vars=["Frequency"], var_name="Tools", value_name="Count")
    fig = px.histogram(d, x="Frequency", y="Count", color="Tools", histfunc="sum", category_orders={"Frequency": ["Hourly", "Daily", "Multiple times per week", "Multiple times per month", "Once per month, or less often"]})
    fig.update_layout(
        xaxis_title=dict(text="Frequency of Spam", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.show()


def scam_exposure():
    answers = []
    for response in final_responses:
        answers.append(response["q9"])
    del answers[2] # removes data irellevant for this plot

    duration = []

    for answer in answers:
        answer = answer[0]
        if "Less" in answer:
            duration.append("Less than a minute")
        elif "A few" in answer:
            duration.append("A few minutes")
        elif "Up to" in answer:
            duration.append("Up to an hour")
        elif "Multiple" in answer:
            duration.append("Multiple hours")
        else:
            duration.append("More than 12 hours")

    freq = []
    for response in final_responses:
        freq.append(response["q8"])
    del freq[2] # removes data irellevant for this plot
    frequency = []
    for f in freq:
        frequency.append(f[0])

    d = pd.DataFrame({"Frequency": frequency, "Duration": duration})
    d_counts = d.groupby(["Frequency", "Duration"]).size().reset_index(name="count")
    d_counts["percentage"] = d_counts.groupby("Frequency")["count"].transform(lambda x: (100*x/x.sum())/100)

    fig = px.bar(d_counts, x="Frequency", y="percentage", color="Duration", category_orders={"Frequency": ["Hourly", "Daily", "Multiple times per week", "Multiple times per month", "Once per month, or less often"], "Duration": ["Less than a minute", "A few minutes", "Up to an hour", "Multiple hours", "More than 12 hours"]})
    fig.update_layout(
        xaxis_title=dict(text="Frequency of Spam", font=dict(size=30)), 
        xaxis=dict(tickfont=dict(size=25)), 
        yaxis_title=dict(text="Nr of servers", font=dict(size=30)), 
        yaxis=dict(tickfont=dict(size=20)),
        legend=dict(font=dict(size=25))
    )
    fig.layout.yaxis.tickformat = '.0%'
    fig.show()


fix_data() # Fix missing Q7 data

final_responses = responses # all valid responses
server_responses = same_server()
final_responses_trimmed = [] # responses without server ID condensed into one answer
for response in server_responses:
    final_responses_trimmed.append(condense(server_responses[response]))

"""
Comment in the functions you want to run below:
"""

q1_barchart()
q2_barchart()
q3_barchart()
q4_barchart()
q5_barchart()
q6_barchart()
q7_barchart()
q8_barchart()
q9_barchart()
q10_barchart()
q11_barchart()
q12_barchart()
sizecomp(True, True, True, True, True) # parameters, in order, are for: bot usage, automod usage, frequency of spam, content of spam, speed of manual spam removal
accessamountcomp()
effectiveness_fail()
effectiveness_prevent()
scam_exposure()
