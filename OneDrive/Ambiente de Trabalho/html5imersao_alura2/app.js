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