document.addEventListener('DOMContentLoaded', function () {
    const cepInput = document.getElementById('id_cep');
    const streetInput = document.getElementById('id_delivery_street');
    const neighborhood = document.getElementById('id_delivery_neighborhood');
    const cityInput = document.getElementById('id_delivery_city');
    const stateInput = document.getElementById('id_delivery_state');
    
    // COnsulta de CEP na API VIA CEP
    function consultarCEP(cep) {
        cep = cep.replace(/\D/g, ''); // somente números
        if (cep.length !== 8) return;

        fetch(`https://viacep.com.br/ws/${cep}/json`)
            .then(response => response.json())
            .then(data => {
                if(!data.erro) {
                    streetInput.value = data.logradouro;
                    neighborhood.value = data.bairro;
                    cityInput.value = data.localidade;
                    stateInput.value = data.uf;
                } else {
                    alert('CEP não encontrado. Por favor, verifique o número!');
                }
            })
            .catch(error => console.error('Erro ao consultar CEP:', error));
    }

    // Máscara simples de CEP
    if (cepInput) {
        cepInput.addEventListener('input', function (e) {
            let cep = e.target.value.replace(/\D/g, '');
            if (cep.length > 8) cep = cep.substring(0, 8);
            if (cep.length === 8) consultarCEP(cep);
            e.target.value = cep.replace(/(\d{5})(\d{3})/, '$1-$2'); // máscara 00000-000
        });
    }

    // Função para puxar fornecedores e preços ao selecionar o produto
    function atualizarProduto(select) {
        const row = select.closest('.item-row');
        const productId = select.value;
        const unitPriceInput = row.querySelector('.unit-price');
        const suppliersCell = row.querySelector('.suppliers-cell');

    if (!productId) {
        unitPriceInput.value = '';
        suppliersCell.innerHTML = 'Selecione o produto...';
        atualizarSubtotal(row);
        return;
    }

    fetch(`/vendas/api/produto/${productId}/`)
        .then(response => {
                if (!response.ok) throw new Error('Produto não encontrado ou erro na API');
                return response.json();
            })
            .then(data => {
                unitPriceInput.value = parseFloat(data.price).toFixed(2);
                suppliersCell.innerHTML = data.suppliers || 'Nenhum fornecedor';
                atualizarSubtotal(row);
            })
            .catch(error => {
                console.error('Erro ao carregar produto:', error);
                suppliersCell.innerHTML = '<span style="color:red; font-weight:bold;">Erro ao carregar dados...</span>';
                console.log("productId:", productId);
            });
}

    const tableBody = document.querySelector('#items-table tbody');

    function adicionarProduto() {
        const totalFormsInput = document.getElementById('id_items-TOTAL_FORMS');
        let totalForms = parseInt(totalFormsInput.value);

        const lastQuantity = document.querySelector(
            `input[name="items-${totalForms - 1}-quantity"]`
        );

        if (!lastQuantity || lastQuantity.value === "") {
            alert("Preencha a quantidade antes de adicionar outro produto.");
            return;
        }

        const tableBody = document.querySelector('#items-table tbody');
        const lastRow = tableBody.querySelector('.item-row:last-child');
        const newRow = lastRow.cloneNode(true);

        newRow.innerHTML = newRow.innerHTML.replace(
            new RegExp(`items-${totalForms - 1}`, 'g'),
            `items-${totalForms}`
        );

        newRow.querySelectorAll('input').forEach(input => {
            input.value = '';
        });

        // reseta selects
        newRow.querySelectorAll('select').forEach(select => {
            select.selectedIndex = 0;
        });

        tableBody.appendChild(newRow);
        totalFormsInput.value = totalForms + 1;
    }


    // Eventos
    tableBody.addEventListener('change', function (e) {
        if (e.target.classList.contains('product-select')) {
            atualizarProduto(e.target);
        }
    });

    tableBody.addEventListener('input', function (e) {
        if (e.target.classList.contains('quantity')) {
            atualizarSubtotal(e.target.closest('.item-row'));
        }
    });

    tableBody.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-row')) {
            e.target.closest('.item-row').remove();
            atualizarTotal();
        }
    });

    // Tornando função visível para o HTML
    window.adicionarProduto = adicionarProduto;


    // Função para calcular o sutotal da linha
    function atualizarSubtotal(row) {
        const quantity = parseInt(row.querySelector('.quantity').value) || 0;
        const price = parseFloat(row.querySelector('.unit-price').value) || 0;
        const subtotal = quantity * price;
        row.querySelector('.subtotal-cell').textContent = 'R$ ' + subtotal.toFixed(2);
        atualizarTotal();
    }

    // Função para calculcar o total da venda
    function atualizarTotal() {
        let total = 0;
        document.querySelectorAll('.subtotal-cell').forEach(cell => {
            const value = parseFloat(cell.textContent.replace('R$ ', '')) || 0;
            total += value;
        });
        document.getElementById('total-venda').textContent = 'R$ ' + total.toFixed(2);
    }

    // Eventos nas linhas existentes
    document.querySelectorAll('.product-select').forEach(select => {
        select.addEventListener('change', function () {
            atualizarProduto(this);
        });
    });

    document.querySelectorAll('.quantity').forEach(input => {
        input.addEventListener('input', function () {
            atualizarSubtotal(this.closest('.item-row'));
        });
    });

    document.querySelectorAll('.remove-row').forEach(btn => {
        btn.addEventListener('click', function () {
            this.closest('.item-row').remove();
            atualizarTotal();
        });
    });

    // Inicializa total
    atualizarTotal();
});