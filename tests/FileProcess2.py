# coding=utf-8
import codecs
import re

monthly = "monthly2.txt"
monthly2 = "monthly3.txt"
deadwood = "deadwoodMonthly2.txt"
deadwood2 = "deadwoodMonthly3.txt"
dailyDelta = "dailyDelta2.txt"
dailyDelta2 = "dailyDelta3.txt"

start = '	<test key="PB_DAILY_Delta_%d" ftp="eqFTP" type="Daily" enable="true" RetestAfterMinutes="20">\r\n' \
        '<description>PB Feed %s Daily Delta File</description>\r\n'

end = '''
<alert method="email">
			<email_address>EquityFeedSupport@morningstar.com</email_address>
			<cc_address></cc_address>
			<subject>Warning: PB Feed Daily %s Delta files have not not uploaded to FTP yet![Daily]</subject>
			<message_body>
        ---------------------------------
        Failure message:{failure_message}
        File name:
        {filename}
        Condition: {condition}
        ---------------------------------

      </message_body>
		</alert>
		<help></help>
		<condition>
			<name>DayOfWeek</name>
			<action>ContinueIfConditionMet</action>
			<param name="Range">mon,tue,wed,thu,fri</param><!-- according file, weekend will not generate file -->
		</condition>
		<condition>
			<name>TimeRange</name>
			<action>ContinueIfConditionMet</action>
			<param name="Start">09:00</param> <!--   Send alert email if files are not ready at 9:00 AM every day -->
			<param name="End">10:00</param>
		</condition>
		<condition>
			<name>FileExists</name>
			<action>AlertIfConditionNotMet</action>
			<param name="DateTime_style"/>
		</condition>
		<condition>
			<name>MinimumFilesize</name>
			<action>AlertIfConditionNotMet</action>
			<param name="Filesize">20</param>
		</condition>
	</test>
'''

file_start = '	<filename filesize="20b">'
file_end = '</filename>\r\n'

country = []


def get_all_country(source):
    try:
        pattern = r'/.*?/([A-Za-z]{3})/Fundamental/.*'
        file_object = codecs.open(source, 'r')
        for line in file_object:
            match_obj = re.match(pattern, line, re.S)
            if match_obj:
                val = match_obj.group(1)
                if val not in country:
                    country.append(val)
        file_object.close()
        return country
    except IOError:
        print "找不这个文件".decode('utf8').encode('gbk')


def process_file(source, target):
    get_all_country(source)
    file_object = codecs.open(source, 'r')
    count = 0
    for c in country:
        count += 1
        content_start = start % (count, c)
        content_end = end % c
        tmp = ''
        for line in file_object:
            if '/'+c+'/' in line:
                tmp = tmp + file_start + line + file_end
        data = '%s%s%s' % (content_start, tmp, content_end)
        write_file(target, data)


def write_file(target, data):
    f = codecs.open(target, 'a', 'utf-8')  # w会清空原来的内容 a为追加
    f.write(str(data) + '\r\n')  # \r\n为换行符
    f.close()


process_file(monthly, monthly2)