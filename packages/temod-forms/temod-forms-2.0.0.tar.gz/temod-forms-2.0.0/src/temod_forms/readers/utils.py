from datetime import datetime, date

class AdaptativeTimeParser(object):
	"""docstring for AdaptativeTimeParser"""

	DATE_FORMATS = [
		"%Y %m %d", "%Y %d %m"
	]

	DURATION_FORMATS = [
		"%H:%M:%S","%H:%M","%M:%S"
	]

	PREDEFINED_TRANSFORMERS = [
		datetime.fromisoformat,
	]

	EMPTY_STRING_IS_NONE = True

	def parse_str(string):
		if string == "" and AdaptativeTimeParser.EMPTY_STRING_IS_NONE:
			return 
		for function in AdaptativeTimeParser.PREDEFINED_TRANSFORMERS:
			try:
				return function(string)
			except:
				pass
		if "T" in string:
			date_part = AdaptativeTimeParser.parse_date_str(string.split('T')[0])
			return datetime.fromtimestamp(
				datetime.fromisoformat(date_part.isoformat()).timestamp()+
				AdaptativeTimeParser.parse_duration_str(string.split('T')[1])
			)
		elif " " in string:
			print("parsing date ",string.split(' '))
			date_part = AdaptativeTimeParser.parse_date_str(string.split(' ')[0])
			return datetime.fromtimestamp(
				datetime.fromisoformat(date_part.isoformat()).timestamp()+
				AdaptativeTimeParser.parse_duration_str(string.split(' ')[1])
			)
		raise Exception(f"Cannot parse time from {string}")

	def parse_date_str(string):
		seps = ["/","-"]; in_ = [sep in string for sep in seps]
		if in_.count(True) != 1:
			raise Exception(f"Cannot parse date from {string}")
		
		sep = seps[in_.index(True)];parts = string.split(sep)
		if len(parts) == 3:
			for date_format in AdaptativeTimeParser.DATE_FORMATS:
				try:
					return datetime.strptime(string.replace(sep," "),date_format).date()
				except:
					pass
		raise Exception(f"Cannot parse date from {string}")

	def parse_duration_str(string):
		for duration_format in AdaptativeTimeParser.DURATION_FORMATS:
			try:
				return datetime.strptime(string,duration_format).timestamp()
			except:
				pass
		raise Exception(f"Cannot parse duration from {string}")


		