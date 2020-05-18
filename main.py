import requests
import dns.resolver
import socket
import smtplib
import csv
# import socks

def guess_emails(company, fn, ln, mn=''):
    emaillist = []
    permlist = get_perms(fn, ln, mn)
    domain = get_domain(company)
    if domain:
        print(domain)
        for perm in permlist:
            email = perm + '@' + domain
            emaillist.append(email)
        try:
            goodemail = verify_email(domain, emaillist)
            print(goodemail)
            return [domain, goodemail]
        except:
            return ["Connection Error"]
    else:
        print("No Domain Found")
        return ["No Domain Found"]


def get_domain(company):
    cbapi = 'https://autocomplete.clearbit.com/v1/companies/suggest?query='
    r = requests.get(cbapi + company)
    try:
        return r.json()[0]["domain"]
    except:
        return None


def get_perms(fn, ln, mn):
    fi = fn[0]
    if len(mn):
        mi = mn[0]
    else:
        mi = ""
    li = ln[0]

    permlist = [fn,
                ln,
                fn + ln,
                fn + '.' + ln,
                fi + ln,
                fi + '.' + ln,
                fn + li,
                fn + '.' + li,
                fi + li,
                fi + '.' + li,
                ln + fn,
                ln + '.' + fn,
                ln + fi,
                ln + '.' + fi,
                li + fn,
                li + '.' + fn,
                li + fi,
                li + '.' + fi,
                fi + mi + ln,
                fi + mi + '.' + ln,
                fn + mi + ln,
                fn + '.' + mi + '.' + ln,
                fn + mn + ln,
                fn + '.' + mn + '.' + ln,
                fn + '-' + ln,
                fi + '-' + ln,
                fn + '-' + li,
                fi + '-' + li,
                ln + '-' + fn,
                ln + '-' + fi,
                li + '-' + fn,
                li + '-' + fi,
                fi + mi + '-' + ln,
                fn + '-' + mi + '-' + ln,
                fn + '-' + mn + '-' + ln,
                fn + '_' + ln,
                fi + '_' + ln,
                fn + '_' + li,
                fi + '_' + li,
                ln + '_' + fn,
                ln + '_' + fi,
                li + '_' + fn,
                li + '_' + fi,
                fi + mi + '_' + ln,
                fn + '_' + mi + '_' + ln,
                fn + '_' + mn + '_' + ln]
    return permlist


def verify_email(domain, emaillist):

    # Sock proxy servers
    # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, '181.101.186.108', 7071)
    # socks.wrapmodule(smtplib)

    try:
        records = dns.resolver.query(domain, 'MX')
    except:
        return "Invalid MX for " + domain

    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    mxcode, message = server.helo(host)
    if mxcode == 250:
        for email in emaillist:
            server.mail('me@domain.com')
            code, message = server.rcpt(str(email))
            print(email, code, message)
            if code == 250:
                server.quit()
                return email
                break
            else:
                pass
        server.quit()
        return 'All Permutations Invalid'

    else:
        return mxcode, message

ifile = open('input 2.csv')
reader = csv.reader(ifile)
ofile = open('output 2.csv', "w")
writer = csv.writer(ofile)
for row in reader:
    output = guess_emails(row[2], row[0], row[1])
    writer.writerow(row + output)
