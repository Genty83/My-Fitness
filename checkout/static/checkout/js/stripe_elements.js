var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
  base: {
    color: '#f1f5f9'
  },
  invalid: {
    color: '#f87171'
  }
};
var card = elements.create('card', {style: style});
card.mount('#card-element')

// Handle errors
card.addEventListener('change', (e) => {
  var errorDiv = document.getElementById('card-errors');
  if (e.error) {
    var html = `
    <span role="alert">
      <i class="fas fa-times ft-red-400"></i>
    </span>
    <span class="ft-red-400">${e.error.message}</span>
    `;
    $(errorDiv).html(html);
  }
  else {
    errorDiv.textContent = '';
  }
});

// Handle form submit 
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(e) {
  e.preventDefault();
  card.update({ 'disabled': true });
  $('#submit-button').attr('disabled', true);
  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
    }
  }).then(function(result) {
    if (result.error) {
      var errorDiv = document.getElementById('card-errors');
      var html = `
        <span role="alert">
          <i class="fas fa-times ft-red-400"></i>
        </span>
        <span class="ft-red-400">${result.error.message}</span>
      `;
      $(errorDiv).html(html);
      card.update({ 'disabled': false });
      $('#submit-button').attr('disabled', false);
    } else {
      if (result.paymentIntent.status === 'succeeded') {
        form.submit();
      }
    }
  })
});