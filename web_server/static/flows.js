var current_compaign = "";		//	current compaign id
var compaigns = Object();		// associative array for compaign-flows
var unsaved_compaign = false;
var flowid = 0;




var _url = "/send_config";

// push compaign config to server
function send_config() {
	var compaign_config = { compaign : compaigns[current_compaign],
							name : current_compaign
						};

	$.ajax({
		type : 'POST',
		url : _url,
		data : JSON.stringify(compaign_config),
		//dataType : 'json',
		contentType : 'application/json',
		success : function() {
			console.log('config sent');
			unsaved_compaign = false;
		},
		error : function() {
			console.log('could not send config');
		}
	});
	//$.blockUI({ message: '<h3 style="color:#3366CC"><img style="height:120px;" src="static/loading2.gif"  />Waiting for results</h3>' });
    $('#myPleaseWait').modal('show');
}

// load past compaigns configs from server
function load_configs() {
	var a = $("#flow_list");

	$.getJSON('/load_configs', function(resp) {
		$.each(resp, function(key, value) {
			a.append($("<p>").html(key + ' ' + value));
		});
	});	

	return false;
}


// save flow configuration
function append_flow(flow_config) {
	var tostring = JSON.stringify(flow_config);
	if(compaigns[current_compaign].indexOf(tostring) != -1) {
		alert('you can\'t define the same flow twice!');
		return;
	}

	console.log('appending flow');
	compaigns[current_compaign].push(tostring);
	var fconfig = $("<p>").html(tostring);
	$('#flows_div').append(fconfig);
}


// utility log function
function LOG(params) {
	for(var i=0; i<params.length; ++i)
		console.log("DEGUB: " + params[i] + "\n")
};


// extracts flow parameters from form
function build_flow() {
	var flow_config = Object();

	var source = $('#source_ip option:selected').val();
	var destination = $("#destination_ip option:selected").val();

	if(source == "" || destination == "") {
		alert("The source and destination ip addresses can\'t be empty.");
		return;
	}

	var protocol =	$('input[name=protocol]:checked').val();


	var trans_duration = $("#trans_duration").val();
	if(!check_param(trans_duration)) {
		alert('invalid trans duration');
		return;
	}

	var sampling_interval = $('#sample_interval').val();
	if(!check_param(sampling_interval)) {
		alert('you didn\'t specify a sampling interval');
		return;
	}

	var metrics = [];
	
	$("#metrics label input").each(function(){
		if($(this).is(":checked")) {
			metrics.push($(this).val());
		}
	});

	if (metrics.length == 0)
	{
		alert('you must choose at least one metric');
		return;
	}
	flow_config.date = Date();
	flow_config.source_ip = source;
	flow_config.destination_ip = destination;
	flow_config.protocol = protocol;
	flow_config.trans_duration = trans_duration;
	flow_config.metrics = metrics;
	flow_config.sampling_interval = sampling_interval;
	if($("#ps_distro_chkb").is(":checked")) {
		flow_config.ps_params = get_parameters_for_distro("ps");
	} else {
		flow_config.ps_params = {'Constant' : $("#packet_size").val()};
	}

	if($("#idt_distro_chkb").is(":checked")) {
		flow_config.idt_params = get_parameters_for_distro("idt");
	} else {
		flow_config.idt_params = {'Constant' : $("#idt").val()};
	}


	append_flow(flow_config);

	if($('#send_config_btn').is('disabled'))
		$('#send_config_btn').prop('disabled', false);

	var flow_entry = $('<button>').attr('data-toggle', 'collapse')
								.attr('data-target', '#flow_'+ flowid+'_description')
								.addClass('btn btn-block')
								.html('Source: '+source +' - Destination: '+destination);

	var flow_description  = $('<div>').attr('id', 'flow_'+ flowid +'_description')
										.addClass('collapse flow_description');
    
    ps_param = '';

	for (var key in flow_config.ps_params)
	{
		if (key == 'Constant')
		ps_param += flow_config.ps_params[key] + ', ';
		else
		for (var k in flow_config.ps_params[key])
		{
			ps_param += k +': '+flow_config.ps_params[key][k] + ', ';
		}
	}

	idt_param = '';
	for (var key in flow_config.idt_params)
	{
		if (key == 'Constant')
		idt_param += flow_config.idt_params[key] + ', ';
		else
		for (var k in flow_config.idt_params[key])
		{
			idt_param += k +': '+flow_config.idt_params[key][k] + ', ';
		}
	}

	ps_param = ps_param.substring(0, ps_param.length - 2);
	idt_param = idt_param.substring(0, idt_param.length - 2);

	var flow_description_html  = '<span class="desc_header">Source IP: </span>' + source + '<br/>';
	flow_description_html += '<span class="desc_header">Destination IP: </span>' + destination + '<br/>';
	flow_description_html += '<span class="desc_header">Protocol: </span>' + protocol + '<br/>';
	flow_description_html += '<span class="desc_header">Packet size: </span>' + Object.keys(flow_config.ps_params)[0] + '<br/>';
	flow_description_html += '<span class="desc_header">Packet size parameters: </span>' + ps_param + '<br/>';
	flow_description_html += '<span class="desc_header">Interdeparture time: </span> '+Object.keys(flow_config.idt_params)[0]+'<br/>';
	flow_description_html += '<span class="desc_header">Interdeparture time parameters: </span>' + idt_param + '<br/>';
	flow_description_html += '<span class="desc_header">Transmission duration: </span>' + trans_duration + '<br/>';
	flow_description_html += '<span class="desc_header">Sampling interval: </span>' + sampling_interval + '<br/>';


	flow_description.html(flow_description_html);

	$("#flow_list").append(flow_entry);
	$("#flow_list").append(flow_description);

	flowid++;

	if($("send_config_btn").is(':disabled'))
		$("send_config_btn").prop('disabled', false);

		$('html, body').animate({
        scrollTop: $("#flow_list").offset().top
    }, 500);
};

// start a new compaign 
function new_compaign() {
	if(unsaved_compaign) {
		// prompt user to either drop or save the compaign
		if(confirm('Are you sure to discard the current config?')) {
			drop_current_compaign();
			initialize_ui();
			if($('#compaign_name').val() == '') return;
		}
		return;
	}

	var compaign_id = $("#compaign_name").val();
	if(!compaign_id) { alert('You didn\'t provide a compaign name'); return; };
	$("#compaign_name").val('');

	if(check_compaign_name(compaign_id)) {
		alert('Invalid compaign name');
		return;
	}

	compaigns[compaign_id] = [];
	current_compaign = compaign_id;

	$("#add_flow_btn").prop('disabled', false);
	$("#compaign_config :input").attr('disabled', false);
    $('#ps_distro_select').prop('disabled', true);
    $('#idt_distro_select').prop('disabled', true);
	unsaved_compaign = true;

	return false;
}

// clear current compaign
function drop_current_compaign() {						//=================== DROP CURRENT COMPAIGN
	compaigns[current_compaign] = [];
	unsaved_compaign = false;
}


$(document).ready(function() {

var checkboxes = $( ':checkbox' );
    checkboxes.prop( 'checked', false );

   ws = new WebSocket("ws://localhost:5000/websocket");

    ws.onopen = function(evt) {
        console.log('socket opened');
        ws.send('first message');
    }
    ws.onmessage = function(evt) {
        $('#myPleaseWait').modal('hide');
        var msg = JSON.parse(evt.data);

        for (var key in msg) {
            $('#graphs').append('<header class="h2 text-center"> flow id: '+key+'</header>');
            $('#graphs').append('<hr>');
            msg[key].forEach(function(entry){

        $('#graphs').append('<div class="graph" id="graph_container'+entry.flow_id+entry.name.replace(/ /g,'')+'"></div><br/><br/>');
        $('#graph_container'+entry.flow_id+entry.name.replace(/ /g,'')).highcharts({
		chart : {
			type : 'line'
		},
		title : {
			text : entry.name + ' between '+entry.sender+' and '+entry.receiver
		},
		xAxis : {
			title : {
				text : '<b>time ('+ entry.unit +')</b>'
			},
			categories: entry.AxeX,

		},
		yAxis : {
		    title : {
				text : '<b>'+entry.name+' (s)</b>'
			},
			labels : {
			     formatter : function() {
                    return this.value.toExponential(2);
                }
            },
		},
		 tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.y} '+entry.unit
        },
        plotOptions: {
            series: {
                minPointLength: 3
            }
        },
		series : [
		{
			name : entry.name,
			data : entry.AxeY
		}],
		lang: {
            noData: "Nichts zu anzeigen"
        },
        noData: {
            style: {
                fontWeight: 'bold',
                fontSize: '15px',
                color: '#303030'
            }
        }
	});
	});
	$('#graphs').append('<hr>');
   }

   $('html, body').animate({
        scrollTop: $("#graphs").offset().top
    }, 500);

 }
    ws.onclose = function(evt) {
        console.log('connexion closed');
        ws = new WebSocket('ws://localhost:8081/websocket');
    }

   /* $('#send_over_ws').click(function() {
        ws.send($('#socket_content').val());
        $('input:first').val('').focus();
        return false;
    });*/

	$("#ps_distro_chkb").click( function(){
	    if( $(this).is(':checked') )
	    {
	        $('#ps_distro_select').prop('disabled', false);
	    }

	   else
	   $('#ps_distro_select').prop('disabled', true);
	});

	$("#idt_distro_chkb").click( function(){
	    if( $(this).is(':checked') ) {
	        $('#idt_distro_select').prop('disabled', false);
	    } else
	   		$('#idt_distro_select').prop('disabled', true);
	});

	// HIDE PS DISTRO ELEMENTS
	$("#ps_distro_params").children().each(function(){
		$(this).hide();
	});

	// HIDE IDT DISTRO ELEMENTS
	$("#idt_distro_params").children().each(function(){
		$(this).hide();
	});


	$("#ps_distro_select").change(function(){
		$("#ps_distro_params").children().each(function(){
				$(this).hide();
		});
		show_relevant_options("ps");
	});

	$("#idt_distro_select").change(function(){
		$("#idt_distro_params").children().each(function(){
				$(this).hide();
		});
		show_relevant_options("idt");
	});


	$("#ps_distro_chkb").change(function() {
		console.log('ps distro changed');
		if($(this).is(':checked')) {
			show_relevant_options("ps");
		} else {
			$("#ps_distro_params").children().each(function(){
				$(this).hide();
			});
		}
	});

	$("#idt_distro_chkb").change(function() {
		console.log('ps distro changed');
		if($(this).is(':checked')) {
			show_relevant_options("idt");
		} else {
			$("#idt_distro_params").children().each(function(){
				$(this).hide();
			});
		}
	});


	// initialise interface
	initialize_ui();

	// hook handlers
	$("#add_flow_btn").click(build_flow);
	$('#new_compaign_btn').click(new_compaign);
	$('#send_config_btn').click(send_config);
	$('#load_config_btn').click(load_configs);
	$('#compaign_config input[name=protocol]').change(function() {
		if(this.value == 'udp_multi') {
			$('#ps_distro_chkb').prop('disabled', true);
			$('#ps_distro_select').prop('disabled', true);
			$('#idt_distro_chkb').prop('disabled', true);
			$('#idt_distro_select').prop('disabled', true);
		} else {
			$('#ps_distro_chkb').prop('disabled', false);
			$('#ps_distro_select').prop('disabled', true);
			$('#idt_distro_chkb').prop('disabled', false);
			$('#idt_distro_select').prop('disabled', false);
		}
	});

	// load available compaign names from database
	$('#load_compaign_btn').click(load_compaign_names);
});

