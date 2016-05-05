var current_compaign = "";		//	current compaign id
var compaigns = Object();		// associative array for compaign-flows
var unsaved_compaign = false;
var flowid = 0;

var _url = "/";

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

	var source = $('#source_ip').val();
	var destination = $("#destination_ip").val();

	if(source == "" || destination == "") {
		alert("The source and destination ip addresses can\'t be empty.");
		return;
	}

	var protocol =	$('input[name=protocol]:checked').val()
	var packet_size = $("#packet_size").val();
	if(!check_param(packet_size)) {
		alert('invalid packet size');
		return;
	}

	var idt = $("#idt").val();
	if(!check_param(idt)) {
		alert('invalid idt');
		return;
	}

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

	if(metrics.length == 0) {
		alert('no metrics specified');
		return;
	}

	flow_config.date = Date();
	flow_config.source_ip = source;
	flow_config.destination_ip = destination;
	flow_config.protocol = protocol;
	flow_config.packet_size = packet_size;
	flow_config.idt = idt;
	flow_config.trans_duration = trans_duration;
	flow_config.metrics = metrics;
	flow_config.sampling_interval = sampling_interval;
	
	if($("#ps_distro_chkb").is(":checked")){
		flow_config.ps_distro = $("#ps_distro_select option:selected").text();
	}

	if($("#idt_distro_chkb").is(":checked")){
		flow_config.idt_distro = $("#idt_distro_select option:selected").text();
	}

	console.log(flow_config);
	append_flow(flow_config);

	if($('#send_config_btn').is('disabled'))
		$('#send_config_btn').prop('disabled', false);

	var flow_entry = $('<button>').attr('data-toggle', 'collapse')
								.attr('data-target', '#flow_'+ flowid+'_description')
								.addClass('btn btn-block')
								.html('Source: '+source +' - Destination: '+destination);

	console.log('flow_'+ flowid);
	console.log(flowid);

	var flow_description  = $('<div>').attr('id', 'flow_'+ flowid +'_description')
										.addClass('collapse flow_description');

	var flow_description_html  = '<span class="desc_header">Source IP: </span>' + source + '<br/>';
	flow_description_html += '<span class="desc_header">Destination IP: </span>' + destination + '<br/>';
	flow_description_html += '<span class="desc_header">Protocol: </span>' + protocol + '<br/>';
	flow_description_html += '<span class="desc_header">Pacet size: </span>' + packet_size + '<br/>';
	flow_description_html += '<span class="desc_header">Interdeparture time: </span>' + idt + '<br/>';
	flow_description_html += '<span class="desc_header">Transmission duration: </span>' + protocol + '<br/>';
	flow_description_html += '<span class="desc_header">Sampling interval: </span>' + sampling_interval + '<br/>';


	flow_description.html(flow_description_html);

	console.log(flow_description.html());
	console.log('appending flow button');

	$("#flow_list").append(flow_entry);
	$("#flow_list").append(flow_description);

	flowid++;

	if($("send_config_btn").is(':disabled'))
		$("send_config_btn").prop('disabled', false);
};

// start a new compaign 
function new_compaign() {
	if(unsaved_compaign) {
		// prompt user to either drop or save the compaign
		if(confirm('Are you sure to discard the current config?')) {
			console.log('dropped current compaign');			
			drop_current_compaign();
			initialize_ui();
			if($('#compaign_name').val() == '') return;
		}
		return;
	}

	var compaign_id = $("#compaign_name").val();
	$("#compaign_name").val('');

	/*if(check_compaign_name(compaign_id)) {
		alert('Invalid compaign name');
		return;
	}*/

	compaigns[compaign_id] = [];
	current_compaign = compaign_id;

	$("#add_flow_btn").prop('disabled', false);
	$("#compaign_config :input").attr('disabled', false);

	unsaved_compaign = true;

	return false;
}

// clear current compaign
function drop_current_compaign() {						//=================== DROP CURRENT COMPAIGN
	compaigns[current_compaign] = [];
	unsaved_compaign = false;
}


$(document).ready(function() {

	// INITIALIZE WEBSOCKET
	 if (!window.WebSocket) {
        if (window.MozWebSocket) {
            window.WebSocket = window.MozWebSocket;
        } else {
            $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
        }
    }



    ws = new WebSocket('ws://localhost:8080/websocket');

    ws.onopen = function(evt) {
        console.log('socket opened');
        ws.send('first message');
    }
    ws.onmessage = function(evt) {
        var msg = JSON.parse(evt.data);
        $('#graph_container').highcharts({
		chart : {
			type : 'line'
		},
		title : {
			text : 'Bandwidth'
		},
		xAxis : {
			title : {
				text : 'time'
			}
		},
		series : [
		{
			name : msg.name,
			data : msg.data
		}
		]
	});
    }
    ws.onclose = function(evt) {
        console.log('connexion closed');
    }

   /* $('#send_over_ws').click(function() {
        ws.send($('#socket_content').val());
        $('input:first').val('').focus();
        return false;
    });*/



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
			$('#ps_distro_select').prop('disabled', false);
			$('#idt_distro_chkb').prop('disabled', false);
			$('#idt_distro_select').prop('disabled', false);
		}
	});

	// load available compaign names from database
	$('#load_compaign_btn').click(load_compaign_names);
});

