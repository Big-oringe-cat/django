		$(document).ready(function(){
			$('input[type=checkbox],input[type=radio],input[type=file]').uniform();			
			$('select').select2();

		    $("#formID").validationEngine();
		    
		    $('.datepicker').datepicker({
				todayBtn: "linked",
			    language: "zh-CN",
			    todayHighlight: true
			});

		});
		$(document).ready(function(){
			$('input[type=checkbox],input[type=radio],input[type=file]').uniform();			
			$('select').select2();
		    $("#formID").validationEngine();
		    
		    var all_check = $(":checkbox[name='all_check']");
		    var server_group = $(".checkbox-group :checkbox[name='serverName']");
		    var user_group = $(".checkbox-group :checkbox[name='groupName']");
		    //全选
		    $(all_check).click(function(){		    	
		    	var check_id = $(this).attr("id");
		    	var group = $(this).parents(".checkbox-group").find(":checkbox[name='"+check_id+"']");
		    	var group_parent = group.parent("span");
		    	var flag = !($(this).attr("checked"));
		    	if (flag == false){
		    		group.add($(this)).attr("checked",true);
		    		group_parent.attr("class","checked");
		    	} else if (flag == true){
		    		group.add($(this)).attr("checked",false);
		    		group_parent.removeAttr("class");
		    	}
		    });
		    //点选
		    server_group.add(user_group).click(function(e){
		    	e.stopPropagation();
		    	var g_parent = $(this).parents(".checkbox-group");
		    	var group_name = $(this).attr("name");
		    	var group = g_parent.find(":checkbox[name='"+group_name+"']");
		    	var g_all_check = g_parent.find(":checkbox[name='all_check']");
		    	var g_all_check_parent = g_all_check.parent("span");
		    	var flag = group.size() == group.filter(':checked').size()
		    	if (flag == true){
		    		g_all_check.attr('checked',true);
		    		g_all_check_parent.attr("class","checked");
		    	}else if (flag == false){
		    		g_all_check.attr("checked",false);
		    		g_all_check_parent.removeAttr("class");
		    	}
		    	
		    });
		});
		