var current_compaign = "";		//	current compaign id
var compaigns = Object();		// associative array for compaign-flows
var unsaved_compaign = false;
var flowid = 0;

var _url = "/start_compaign";

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
	$.blockUI({ message: '<h3 style="color:#3366CC"><img style="height:120px;" src="static/loading2.gif"  />Waiting for results</h3>' });

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


	var packet_size = $("#packet_size").val();
	var min_rate = $("#mi_rate_idt").val();

	var max_rate = $("#ma_rate_idt").val();

	/*if(!check_param(packet_size)) {
		alert('invalid packet size');
		return;
	}*/

	var idt = $("#idt").val();
	var rate = $("#ra_ps").val();
	/*if(!check_param(idt)) {
		alert('invalid idt');
		return;
	}*/

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

	flow_config.date = Date();
	flow_config.source_ip = source;
	flow_config.destination_ip = destination;
	flow_config.protocol = protocol;
	flow_config.trans_duration = trans_duration;
	flow_config.metrics = metrics;
	flow_config.sampling_interval = sampling_interval;
	
	if($("#ps_distro_chkb").is(":checked")){
		flow_config.ps_distro = $("#ps_distro_select option:selected").val();
	}

	if($("#idt_distro_chkb").is(":checked")){
		flow_config.idt_distro = $("#idt_distro_select option:selected").val();

	}
    var tab = [min_rate,max_rate];
    console.log(flow_config.ps_distro);
	if (flow_config.ps_distro=='-e')
	flow_config.packet_size = [rate];
	else
	flow_config.packet_size =[packet_size];

	if (flow_config.idt_distro=='-U')
	flow_config.rate = tab;
	else
	flow_config.rate =[idt];





	console.log(flow_config);
	append_flow(flow_config);

	if($('#send_config_btn').is('disabled'))
		$('#send_config_btn').prop('disabled', false);

	var flow_entry = $('<button>').attr('data-toggle', 'collapse')
								.attr('data-target', '#flow_'+ flowid+'_description')
								.addClass('btn btn-block')
								.html('Source: '+source +' - Destination: '+destination);

	console.log('flow_'+ flowid);


	var flow_description  = $('<div>').attr('id', 'flow_'+ flowid +'_description')
										.addClass('collapse flow_description');
    var ps_distro = '';
    if (flow_config.ps_distro =='-e') ps_distro = 'Exponential';
    else ps_distro = 'Constant';
    var idt_distro = '';
    if (flow_config.idt_distro =='-U') idt_distro = 'Uniform';
    else idt_distro = 'Constant';
	var flow_description_html  = '<span class="desc_header">Source IP: </span>' + source + '<br/>';
	flow_description_html += '<span class="desc_header">Destination IP: </span>' + destination + '<br/>';
	flow_description_html += '<span class="desc_header">Protocol: </span>' + protocol + '<br/>';
	flow_description_html += '<span class="desc_header">Pacet size: </span>' + ps_distro + '<br/>';
	flow_description_html += '<span class="desc_header">lambda: </span>' + packet_size + '<br/>';
	flow_description_html += '<span class="desc_header">Interdeparture time: </span> '+idt_distro+'<br/>';
	flow_description_html += '<span class="desc_header">lambda: </span>' + idt + '<br/>';
	flow_description_html += '<span class="desc_header">Transmission duration: </span>' + trans_duration + '<br/>';
	flow_description_html += '<span class="desc_header">Sampling interval: </span>' + sampling_interval + '<br/>';


	flow_description.html(flow_description_html);

	console.log(flow_description.html());
	console.log('appending flow button');

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
	// INITIALIZE WEBSOCKET
	 if (!window.WebSocket) {
        if (window.MozWebSocket) {
            window.WebSocket = window.MozWebSocket;
        } else {
            $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
        }
    }



    ws = new WebSocket('ws://localhost:8081/websocket');

    ws.onopen = function(evt) {
        console.log('socket opened');
        ws.send('first message');
    }
    ws.onmessage = function(evt) {
        $.unblockUI();
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
				text : '<b>time (s)</b>'
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
            pointFormat: '{point.y} s'
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
    if( $(this).is(':checked') )
    {
        $('#idt_distro_select').prop('disabled', false);
    }

   else
   $('#idt_distro_select').prop('disabled', true);
});


$( "#ps_distro_select" )
  .change(function () {
    var str = "";
    $( "select option:selected" ).each(function() {
      if($( this ).text() == "Exponential")
      {
        $('#rate_ps').fadeIn("slow");
      }
    });
  })
  .change();

  $( "#idt_distro_select" )
  .change(function () {
    var str = "";
    $( "select option:selected" ).each(function() {
      if($( this ).text() == "Uniform")
      {
        $('#min_rate_idt').fadeIn("slow");
        $('#max_rate_idt').fadeIn("slow");
      }
    });
  })
  .change();


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

