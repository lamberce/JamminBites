siteUrl = "http://ec2-52-32-29-152.us-west-2.compute.amazonaws.com:8080/";
$(document).ready(function() { 
		$(".addToCartButton").click(function() {
			$.post(siteUrl + "addToCart", this.id);
		})
})