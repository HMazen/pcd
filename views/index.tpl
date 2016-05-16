<!DOCTYPE html>
<html>
<head>
	<title>Login</title>
	<meta http-equiv="X-UA-Compatible" content="IE=edge" charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
</head>
<body>

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
		<div class="row">
			<div class="text-center col-md-6 col-md-offset-3">
				<br/><br/>
				<img src="shinken_logo.png"/>
				<h4>Traffic Generation<br/>and Performance Measuring Module</h4>
				<br><br>
				<form action ="/" method="POST">
				<input name="login" class="form-control" placeholder="Username"></input><br/>
				<input name="password" class="form-control" placeholder="Password"></input><br/>
				<button id="new_compaign_btn" class="btn btn-info btn-md btn-block">Login</button><br/>
				</form>
			</div>
		</div>
	</div>

</body>
</html>