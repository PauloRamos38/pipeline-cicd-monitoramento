document.addEventListener('DOMContentLoaded', function() {

	// --- Lógica para o formulário de contato (index.html) ---
	const contactForm = document.getElementById('contactForm');
	if (contactForm) {
		contactForm.addEventListener('submit', function(e){
		  e.preventDefault();
		  const nome = document.getElementById('nome').value || 'amigo';
		  alert('Obrigado, ' + nome + '! Sua mensagem foi recebida (exemplo).');
		  this.reset();
		});
	}

	// --- Lógica para o botão "Adicionar ao Carrinho" (páginas de produto) ---
	const addToCartButton = document.querySelector('.add-to-cart');
	if (addToCartButton) {
		addToCartButton.addEventListener('click', function(event) {
			event.preventDefault();
			
			const productName = document.querySelector('.product-info h2').textContent;
			const sizeElement = document.getElementById('tamanho');
			let alertMessage = `"${productName}" foi adicionado ao carrinho! (Exemplo)`;

			// Verifica se existe um seletor de tamanho na página
			if (sizeElement) {
				const selectedSize = sizeElement.value;
				alertMessage = `"${productName}" (Tamanho: ${selectedSize}) foi adicionado ao carrinho! (Exemplo)`;
			}
			
			addToCartButton.textContent = 'Adicionado!';
			addToCartButton.style.backgroundColor = '#059669';
			alert(alertMessage);
		});
	}

	// --- Lógica para carregar o Google Map (index.html) ---
	const mapElement = document.getElementById('map');
	if (mapElement && typeof API_KEY !== 'undefined' && API_KEY !== 'SUA_CHAVE_API_AQUI') {
		// Cria a tag de script para a API do Google Maps
		const script = document.createElement('script');
		script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&callback=initMap`;
		script.async = true;
		script.defer = true;
		
		// Adiciona o script ao final do body
		document.body.appendChild(script);
	} else if (mapElement) {
		mapElement.innerHTML = '<p style="text-align:center; padding-top: 20px;">Mapa indisponível. Configure a chave de API no arquivo <strong>config.js</strong>.</p>';
	}
});

// --- Função para iniciar o Google Map (index.html) ---
// Esta função é chamada pelo script do Google Maps quando ele termina de carregar
function initMap() {
	// Coordenadas de exemplo (Avenida Paulista, São Paulo)
	const location = { lat: -23.561, lng: -46.656 };
	
	// Cria o mapa, centralizado na localização definida
	const map = new google.maps.Map(document.getElementById("map"), {
		zoom: 15,
		center: location,
	});
}