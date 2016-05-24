var past_compaigns = new Array();


function initialize_ui() {
	$("#add_flow_btn").prop('disabled', true);
	//$("#send_config_btn").prop('disabled', true);
	$("#compaign_config :input").attr("disabled", true);

}

// input parameter validation
function check_param(param) {
	if(param == "") return false;
	return true;
};


function check_compaign_name(compaign_name) {				// handle this once db is ready
	var result = false;
	var data = Object();
	data.name = compaign_name;

	$.ajax({
		url : '/check_compaign',
		data : JSON.stringify(data),
		type : 'POST',
		dataType : 'json',
		contentType : 'application/json',
		success : function(resp) {
			console.log(resp['result']);
			if(resp['result'] == 'true') result = true;
			else result = false;
		}
	});

	return result;
}

function process_past_compaigns(resp) {
	var past_compaign = JSON.parse(resp);
}


function load_compaign_names() {
	var comps = Object();
	$.get('/load_past_compaigns', function(resp) {
		var temp = JSON.parse(resp);
		var prompt_string = '';

		for(var i=0; i<temp.compaigns.length; ++i){
			prompt_string += (i+1) + '. ' +temp.compaigns[i]  +'\n';
		}

		if(prompt_string == ''){
			alert('There are no compaigns to load');
			return;
		}

		var answer = prompt('Enter a compaign number::\n\n' + prompt_string + '\n');
		answer = parseInt(answer);

		if(answer < 0 || answer >= temp.compaigns.length) {
			alert('Invalid index');
			return;
		}

		var compaign_name = temp.compaigns[answer-1];
		var data = {'comaign_name' : compaign_name};

		$.ajax({
			url : '/load_compaign_config',
			dataType : 'json',
			contentType : 'application/json',
			type : 'POST',
			data : JSON.stringify(data),
			success : process_past_compaigns(resp)
		});

	});

	console.log(past_compaigns);

	
}

function show_relevant_options(slc) {
	var selector = "#"+slc+"_distro_params";
	switch($("#"+slc+"_distro_select option:selected").text()) {
		case 'Exponential': $(selector+" #expo_params").fadeIn(300); break;
		case 'Uniform': 	$(selector+" #uniform_params").fadeIn(300); break;
		case 'Gamma': 		$(selector+" #gamma_params").fadeIn(300); break;
		case 'Poisson': 	$(selector+" #poisson_params").fadeIn(300); break;
		case 'Cauchy': 		$(selector+" #cauchy_params").fadeIn(300); break;
		case 'Weibull': 	$(selector+" #weibull_params").fadeIn(300); break;
		case 'Pareto':  	$(selector+" #pareto_params").fadeIn(300); break;
		case 'Normal':  	$(selector+" #normal_params").fadeIn(300); break;
		default: break;
	}
}


function get_parameters_for_distro(slc) {
	var selector = "#"+slc+"_distro_params";
	var params = Object();
	switch($("#"+slc+"_distro_select option:selected").text()) {
		case 'Exponential': params['Exponential'] = {'mean_rate' : $(selector+" #expo_mean").val()}; break;
		case 'Uniform': 	params['Uniform'] = {'min_rate' : $(selector+" #uniform_min_rate").val(), 'max_rate': $(selector+" #uniform_max_rate").val()}; break;
		case 'Gamma': 		params['Gamma'] = {'shape' : $(selector+" #gamma_shape").val(), 'scale' : $(selector+" #gamma_scale").val()}; break;
		case 'Poisson': 	params['Poisson'] = {'mean': $(selector+" #poisson_mean").val()}; break;
		case 'Cauchy': 		params['Cauchy'] = {'shape' : $(selector+" #cauchy_shape").val(), 'scale' : $(selector+" #chauchy_scale").val()}; break;
		case 'Weibull': 	params['Weibull'] = {'shape' : $(selector+" #weibull_shape").val(), 'scale' : $(selector+" #weibull_scale").val()}; break;
		case 'Pareto':  	params['Pareto'] = {'shape' : $(selector+" #pareto_shape").val(), 'scale': $(selector+" #pareto_scale").val()}; break;
		case 'Normal':  	params['Normal'] = {'sigma' : $(selector+" #normal_sigma").val(), 'mu' : $(selector+" #normal_mu").val()}; break;
		default: break;
	}

	return params;
}