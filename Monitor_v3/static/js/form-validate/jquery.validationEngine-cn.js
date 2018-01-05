

(function($) {
	$.fn.validationEngineLanguage = function() {};
	$.validationEngineLanguage = {
		newLang: function() {
			$.validationEngineLanguage.allRules = 	{
					"required":{    			// Add your regex rules here, you can take telephone as an example
						"regex":"none",
						"alertText":"* 该项为必选项",
						"alertTextCheckboxMultiple":"* 请选择",
						"alertTextCheckboxe":"* 请选择"},
					"kWord":{
							"regex":"/^(\\(([a-zA-Z0-9_\\u4e00-\\u9fa5]+\\|)*[a-zA-Z0-9_\\u4e00-\\u9fa5]+\\)&)*\\(([a-zA-Z0-9_\\u4e00-\\u9fa5]+\\|)*[a-zA-Z0-9_\\u4e00-\\u9fa5]+\\)|[a-zA-Z0-9_\\u4e00-\\u9fa5]+$/",
							"alertText":"* 格式不规范"},	
					"length":{
						"regex":"none",
						"alertText":"*您输入的字符长度不正确，请确保长度在 ",
						"alertText2":" 和 ",
						"alertText3": " 之间"},
					"length1":{
						"regex":"none",
						"alertText":"*请选择客服和市场"},
					"maxCheckbox":{
						"regex":"none",
						"alertText":"* 您选取的选项过多，请重新选择"},	
					"minCheckbox":{
						"regex":"none",
						"alertText":"* 您选取的选项过少,至少选择 ",
						"alertText2":" 项"},	
					"confirm":{
						"regex":"none",
						"alertText":"* 您两次填写的内容不完全一致，请重新填写"},	
//从telephone往下，除了validate2fields，都需要写成如：custom[telephone]的样式
//custom与funcCall的差别在于，custom是使用正则表达式进行验证即可，而funcCall需要写js函数来进行验证。				
					"telephone":{
							/*"regex":"\d{3}-\d{8}|\d{4}-\d{7}|\d{8}|\d{7}",*/
						"regex":"/^0{0,1}1[0-9]{10}$/",
						"alertText":"* 无效的电话号码，请重新填写"},	
					"email":{
						"regex":"/^[a-zA-Z0-9_\.\-]+\@([a-zA-Z0-9\-]+\.)+[a-zA-Z0-9]{2,4}$/",
						"alertText":"* 无效的邮件地址，请重新填写"},	
					"date":{
                         "regex":"/^[0-9]{4}\-\[0-9]{1,2}\-\[0-9]{1,2}$/",
                         "alertText":"* 日期格式错误，请按照 2012-12-21 这样的格式填写"},
                    "ip":{
                         "regex":"/^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$/",
                         "alertText":"* ip填写错误，请正确填写ip地址"},
					"onlyNumber":{
						"regex":"/^[0-9\ ]+$/",
						"alertText":"* 只能输入数字"},	
					"onlyNumber2":{
							"regex":"/^[-+]?[0-9\ ]+$/",
							"alertText":"* 只能输入数字,包含正负数"},
					"onlyNumber3":{
								"regex":"/^[-+]?[0-9\ ]+.?[0-9\ ]{0,3}$/",
								"alertText":"* 只能输入数字,包含小数,小数后三位"},
					"onlyNumber4":{
									"regex":"/^[0-9\ ]+.?[0-9\ ]{0,3}$/",
									"alertText":"* 不能为负数"},
					"onlyNumber5":{
										"regex":"/^[0-9\ ]+.?[0-9\ ]{0,3}$/",
										"alertText":"* 不能为负数,请检查数据"},
					"onlyNumber9":{
								"regex":"/^[-+]?[0-9\ ]+.?[0-9\ ]{0,4}$/",
								"alertText":"* 只能输入数字,包含小数,小数后四位"},					
					"onlyNumber10":{
								"regex":"/(^[1-9]$)|(^10$)/",
								"alertText":"* 只能输入1-10之间的数字数字"},	
					"onlyNumber11":{
								"regex":"/(^[0-9]$)|(^10$)/",
								"alertText":"* 只能输入0-10之间的数字数字"},					
					"onlyNumber86400":{
								"regex":"/(^[1-9]\\d{0,3}$)|(^[1-7]\\d{4}$)|(^8[0-5]\\d{3}$)|(^86[0-3]\\d{2}$)|(^863[0-2]\\d$)|(^86400$)/",
								"alertText":"* 只能输入1-86400之间的数值"},					
					"noSpecialCaracters":{
						"regex":"/^.{1,20}$/",
						"alertText":"* 1-20个字符"},
						/*"noSpecialCaracters":{
						"regex":"/^[0-9a-zA-Z]+$/",
						"alertText":"* 该项只接受数字和字母的输入"},*/	
				   "ajaxFinanceInfo":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，用户名可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该用户名已被占用，请换个名字试试"},
					"ajaxSmsUser":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，用户名可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该用户名已被占用，请换个名字试试"},
					"ajaxAdminUser":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，可以使用填写的信息",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该信息已经被占用，请换个信息试试"},
					"ajaxCmppUser":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该用户id可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该用户id已被占用，请换个id试试"},
					"ajaxSmgpUser":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该用户id可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该用户id已被占用，请换个id试试"},
					"ajaxSgipUser":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该用户id可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该用户id已被占用，请换个id试试"},
					"ajaxSmsUser":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该用户id可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该用户id已被占用，请换个id试试"},
					"ajaxMmsUser":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该用户id可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该用户id已被占用，请换个id试试"},
					"ajaxGateTd":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该通道代码可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该通道代码已被占用，请换个id试试"},
							
					"ajaxSpTd":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该通道代码可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该通道代码已被占用，请换个id试试"},	
					"ajaxThreadId":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，该线程ID可用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该扫描线程已被占用，请换个id试试"},
					"ajaxPortId":{
							"file":"validate.do",
							"extraData":"type=ajax",
							"alertTextOk":"* 恭喜，端口没有被监控",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该端口已经被监控!"},	
					"ajaxUserSpNumber":{
							"file":"validate.do",
							"extraData":"type=ajaxExt",
							"alertTextOk":"* 恭喜，该接入号可以使用",	
							"alertTextLoad":"* 正在验证，请等待",
							"alertText":"* 该接入号填写错误，请换个接入号试试"},	
								
					"onlyLetter":{
						"regex":"/^[a-zA-Z\ \']+$/",
						"alertText":"* 只能输入字母"},
					"validateStatus":{
    					"nname":"validateClientCount",
    					"alertText":"*输入的状态不符合要求"}	
					}	
			
			
					
		}
	}
})(jQuery);

$(document).ready(function() {	
	$.validationEngineLanguage.newLang()
});