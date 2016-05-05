<!DOCTYPE html>
<html>
<head>
	<title>bootstrap</title>
	<meta http-equiv="X-UA-Compatible" content="IE=edge" charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
	<!--<link rel="stylesheet" type="text/css" href="{{ url('static', filename='styles.css') }}">-->
	<link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>
<body>

	<!-- navbar declarartion -->
	<nav class="navbar navbar-default">
		<div class="container">
			<header class="navbar-header">
				<a href="#" class="navbar-brand">TrafficGen</a>
			</header>
			<div class="collapse navbar-collapse">
				<ul class="nav navbar-nav">
					<li><a href="#">Compaigns</a></li>
					<li><a href="#">Results</a></li>
				</ul>
			</div>
		</div>
	</nav>

	<div class="container col-md-8 col-md-offset-2">
		
		<header class="text-center h1">New Compaign</header>
		<br/><br/>

		<div class="row">
			<div class="text-center col-md-6 col-md-offset-3">
				<label for="compaign_name">Enter the compaign name</label>
				<input id="compaign_name" class="form-control" placeholder="compaign name"></input><br/>
				<button id="new_compaign_btn" class="btn btn-info btn-md btn-block">Start compaign</button><br/>
				<button id="load_compaign_btn" class="btn btn-success btn-md btn-block">Load Compaign</button>
			</div>
		</div>
		<br/><hr><br/>
		<div class="row">
			<div class="col-md-6">
				<form id="compaign_config">

					<label>Protocol</label>
					<div class="radio">
					  <label>
					    <input type="radio" name="protocol" id="optionsRadios1" value="tcp" checked>
					    TCP
					  </label>
					</div>
					<div class="radio">
					  <label>
					    <input type="radio" name="protocol" id="optionsRadios2" value="udp">
					    UDP
					  </label>
					</div>
					<div class="radio">
					  <label>
					    <input type="radio" name="protocol" id="optionsRadios2" value="udp_multi">
					    UDP Multicast
					  </label>
					</div>
					<br/>
				  <div class="form-group">
				    <label for="source_ip">Source IP</label>
				    <input type="text" class="form-control" id="source_ip" placeholder="localhost">
				  </div>
				  <div class="form-group">
				    <label for="destination_ip">Destination IP</label>
				    <input type="text" class="form-control" id="destination_ip" placeholder="localhost">
				  </div>
				  <div class="form-group">
				    <label for="packet_size">Packet size (bytes)</label>
				    <input type="text" class="form-control" id="packet_size" placeholder="500">
				  </div>
				  <label>Use PS distrobution</label>
				  <div class="checkbox" >
					  <label>
					    <input type="checkbox" id="ps_distro_chkb" value="">
						Enable		
					  </label>
					  <select class="form-control" id="ps_distro_select">
						  <option>Gamma</option>
						  <option>Uniform</option>
						  <option>Noramal</option>
						  <option>Cauchy</option>
						  <option>Constant</option>
						  <option>Exponential</option>
					 </select><br>
					Rate: &lambda;&nbsp;<input type="text" width="20">
					</div>
					<div class="form-group">
				    <label for="idt">Inter-departure time (ms)</label>
				    <input type="text" class="form-control" id="idt" placeholder="50">
				  </div>

				  <label>Use IDT distrobution</label>
				  <div class="checkbox">
					  <label>
					    <input type="checkbox" id="idt_distro_chkb" value="">
						Enable		
					  </label>
					  <select class="form-control" id="idt_distro_select">
						  <option>Gamma</option>
						  <option>Uniform</option>
						  <option>Noramal</option>
						  <option>Cauchy</option>
						  <option>Constant</option>
						  <option>Exponential</option>
					 </select><br>
					Rate: &lambda;&nbsp;<input type="text" width="20">
					</div>
					<label>Metrics</label><br/>
					<div id="metrics">
						<label>
						    <input type="checkbox" id="bandwidth_chkb" value="bandwidth">
							Bandwidth		
						 </label><br/>
						 <label>
						    <input type="checkbox" id="jitter_chkb" value="jitter">
							Jitter		
						 </label><br/>
						 <label>
						    <input type="checkbox" id="loss_chkb" value="loss_rate">
							Loss rate		
						 </label><br/>
						 <label>
						    <input type="checkbox" id="rtd_chkb" value="rtd">
							Round trip delay	
						 </label>
						 </div>
						 <br/><br/>
						 <div class="form-group">
					    <label for="sample_interval">Sampling interval (ms)</label>
					    <input type="text" class="form-control" id="sample_interval" placeholder="100ms">

					    <label for="trans_duration">Sampling interval (ms)</label>
					    <input type="text" class="form-control" id="trans_duration" placeholder="1min">
				  	</div>
				  		
				  	
				</form></div>
			<div class="col-md-6 scrollable" id="flow_list">
				
			</div>

		</div>

		<div class="row">
			
			<button id="add_flow_btn" class="col-md-offset-1 col-md-4 btn btn-default">Add new flow</button>
			<div class="col-md-2"></div>
			<button id="send_config_btn" class="col-md-4 btn btn-default btn-success">Send configuration</button>

		</div>

		<br/><br/><br/><br/>
		<hr>
		<br/>
		<div class="row">
			<header class="h1 text-center">Compaign Results</header>
			<div id="graph_container">
				<!-- graph will go here -->
			</div>
			<br/><br/>
		</div>

	</div>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="{{ url('static', filename='jquery-2.2.2.js') }}"></script>
	<script type="text/javascript" src="{{ url('static', filename='utilities.js') }}"></script>
	<script type="text/javascript" src="{{ url('static', filename='flows.js') }}"></script>
	<script type="text/javascript" src="{{ url('static', filename='highcharts.js') }}"></script>

</body>
</html>
