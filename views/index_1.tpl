<!DOCTYPE html>
<html>
<head>
	<title>bootstrap</title>
	<meta http-equiv="X-UA-Compatible" content="IE=edge" charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='styles.css') }}">

	<!--<link rel="stylesheet" type="text/css" href="/static/styles.css">-->
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
					<li><a href="#compaings">Compaigns</a></li>
					<li><a href="#results">Results</a></li>
				</ul>
				<ul class="nav navbar-nav navbar-right">
                <li><a href="/logout">Logout</a></li>
                </ul>
			</div>
		</div>
	</nav>

	<div class="container col-md-8 col-md-offset-2">
		
		<header class="text-center h1"><a name="compaigns">New Compaign</a></header>
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
					    <input type="radio" name="protocol" id="optionsRadios1" value="TCP" checked>
					    TCP
					  </label>
					</div>
					<div class="radio">
					  <label>
					    <input type="radio" name="protocol" id="optionsRadios2" value="UDP">
					    UDP
					  </label>
					</div>
					<div class="radio">
					  <label>
					    <input type="radio" name="protocol" id="optionsRadios2" value="Multicast">
					    UDP Multicast
					  </label>
					</div>
					<br/>
				  <div class="form-group">
				    <label for="source_ip">Source IP</label>
				    <select class="form-control" id="source_ip">
						  <option value ="192.168.56.1">192.168.56.1</option>
						  <option value="192.168.56.101">192.168.56.101</option>
						  <option value="192.168.56.102">192.168.56.102</option>
						  <option value="192.168.56.103">192.168.56.103</option>
					 </select>
				  </div>


				 <div class="form-group">
				    <label for="destination_ip">Destination IP</label>
                    <select class="form-control" id="destination_ip">
						  <option value ="192.168.56.1">192.168.56.1</option>
						  <option value="192.168.56.101">192.168.56.101</option>
						  <option value="192.168.56.102">192.168.56.102</option>
						  <option value="192.168.56.103">192.168.56.103</option>
					 </select>				  
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
					  <br><br>
					  <select class="form-control" id="ps_distro_select">
						  <option value ="-g">Gamma</option>
						  <option value="-u">Uniform</option>
						  <option value="-n">Normal</option>
						  <option value="-y">Cauchy</option>
						  <option value="-e">Exponential</option>
						  <option value="-v">Pareto</option>
						  <option value="-w">Weibull</option>
						  <option value="-o">Poisson</option>
					 </select>

					<div id="ps_distro_params">
						<div id = "expo_params">
							<br>Mean rate &lambda;&nbsp;<input id = "expo_mean_rate" type="text" width="20"/>
						</div>

						<div id = "gamma_params">
							<br>Shape &alpha;&nbsp;<input id = "gamma_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;&nbsp;<input id = "gamma_scale" type="text" width="20"/>
						</div>

						<div id = "uniform_params">
							<br>Min rate &alpha;&nbsp;<input id = "uniform_min_rate" type="text" placeholder="500" width="20"/>
							<br>Max rate &beta;&nbsp;<input id = "uniform_max_rate" type="text" placeholder="1000" width="20"/>
						</div>

						<div id = "cauchy_params">
							<br>Shape &alpha;&nbsp;<input id = "cauchy_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;&nbsp;<input id = "cauchy_scale" type="text" width="20"/>
						</div>

						<div id = "normal_params">
							<br>Std. dev. &sigma;&nbsp;<input id = "normal_sigma" type="text" width="20"/>
							<br>Mean &mu;&nbsp;<input id = "normal_mu" type="text" width="20"/>
						</div>

						<div id = "poisson_params">
							<br>Mean &lambda;&nbsp;<input id = "poisson_mean" type="text" width="20"/>
						</div>

						<div id = "pareto_params">
							<br>Shape &alpha;&nbsp;<input id = "pareto_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;&nbsp;<input id = "pareto_scale" type="text" width="20"/>
						</div>

						<div id = "weibull_params">
							<br>Shape &alpha;&nbsp;<input id = "weibull_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;&nbsp;<input id = "weibull_scale" type="text" width="20"/>
						</div>

					</div> <!-- ============================== PACKET SIZE DISTRO PARAMETERS -->

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
					  <br><br>
					  <select class="form-control" id="idt_distro_select">
						  <option value ="-G">Gamma</option>
						  <option value="-U">Uniform</option>
						  <option value="-N">Normal</option>
						  <option value="-Y">Cauchy</option>
						  <option value="-E">Exponential</option>
						  <option value="-V">Pareto</option>
						  <option value="-O">Poisson</option>
					 </select>
					 
					 <div id="idt_distro_params">
						<div id = "expo_params">
							<br>Mean rate &lambda;&nbsp;<input id = "expo_mean_rate" type="text" width="20"/>
						</div>

						<div id = "gamma_params">
							<br>Shape &alpha;&nbsp;<input id = "gamma_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;<input id = "gamma_scale" type="text" width="20"/>
						</div>

						<div id = "uniform_params">
							<br>Min rate &alpha;&nbsp;<input id = "uniform_min_rate" type="text" placeholder="500" width="20"/>
							<br>Max rate &beta;&nbsp;<input id = "uniform_max_rate" type="text" placeholder="1000" width="20"/>
						</div>

						<div id = "normal_params">
							<br>Std. dev. &sigma;&nbsp;<input id = "normal_sigma" type="text" width="20"/>
							<br>Mean &mu;&nbsp;<input id = "normal_mu" type="text" width="20"/>
						</div>

						<div id = "poisson_params">
							<br>Mean &lambda;&nbsp;<input id = "poisson_mean" type="text" width="20"/>
						</div>

						<div id = "cauchy_params">
							<br>Shape &alpha;&nbsp;<input id = "cauchy_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;&nbsp;<input id = "cauchy_scale" type="text" width="20"/>
						</div>

						<div id = "pareto_params">
							<br>Shape &alpha;&nbsp;<input id = "pareto_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;&nbsp;<input id = "pareto_scale" type="text" width="20"/>
						</div>

						<div id = "weibull_params">
							<br>Shape &alpha;&nbsp;<input id = "weibull_shape" type="text" width="20"/>
							<br>Scale &beta;&nbsp;&nbsp;&nbsp;<input id = "weibull_scale" type="text" width="20"/>
						</div>

					</div> <!-- ============================== INTERDEPARTURE TIME DISTRO PARAMETERS -->


					</div>
					<label>Metrics</label><br/>
					<div id="metrics">
						<label>
						    <input type="checkbox" id="bandwidth_chkb" value="bit rate">
							Bandwidth		
						 </label><br/>
						 <label>
						    <input type="checkbox" id="jitter_chkb" value="jitter">
							Jitter		
						 </label><br/>
						 <label>
						    <input type="checkbox" id="loss_chkb" value="packet loss">
							Loss rate		
						 </label><br/>
						 <label>
						    <input type="checkbox" id="rtd_chkb" value="delay">
							Round trip delay	
						 </label>
						 </div>
						 <br/><br/>
						 <div class="form-group">
					    <label for="sample_interval">Sampling interval (ms)</label>
					    <input type="text" class="form-control" id="sample_interval" placeholder="100ms">

					    <label for="trans_duration">Duration (s)</label>
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
		<div class="row" id="graphs">
			<header class="h1 text-center"><a name="results">Compaign Results</a></header>
		</div>

	</div>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="{{ url('static', filename='jquery-2.2.2.js') }}"></script>
	<script type="text/javascript" src="{{ url('static', filename='utilities.js') }}"></script>
	<!-- <script src="../static/utilities.js"></script> -->
	<script type="text/javascript" src="{{ url('static', filename='jquery.blockUI.js') }}"></script>
	<script type="text/javascript" src="{{ url('static', filename='flows.js') }}"></script>
	<!-- <script src="../static/flows.js"></script> -->
	<script type="text/javascript" src="{{ url('static', filename='highcharts.js') }}"></script>

</body>
</html>
