siteUrl = "http://ec2-52-32-29-152.us-west-2.compute.amazonaws.com:8080/";
$(document).ready(function() { 
		$(".addToCartButton").click(function() {
			$.ajax({
				url: siteUrl + "addToCart",
				method: "POST",
				data: {itemId : this.id}
			})
		});
});

$(document).ready(function() {
	$("#submitButton").click(function() {
		window.location.reload();
	});
});