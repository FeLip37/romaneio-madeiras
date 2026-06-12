# -*- coding: utf-8 -*-
"""ROMANEIO.ipynb"""

def calcular_romaneio_lote():
    print("--- Calculadora Automática de Romaneio ---")

    try:
        largura = float(input("Digite a largura da madeira (ex: 15): "))
        espessura = float(input("Digite a espessura da madeira (ex: 5): "))

        largura_m = largura / 100
        espessura_m = espessura / 100

        comprimentos = [
            1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50,
            5.00, 5.50, 6.00, 6.50, 7.00, 7.50, 8.00
        ]

        volume_total = 0.0

        print("\n--- Digite a quantidade de peças para cada comprimento ---")
        print("(Se não houver peças de um tamanho, digite 0 ou apenas aperte Enter)")

        for comp in comprimentos:
            entrada = input(f"Quantidade de peças com {comp:.2f}m: ")

            if not entrada.strip():
                qtd = 0
            else:
                qtd = int(entrada)

            if qtd > 0:
                volume_item = largura_m * espessura_m * comp * qtd
                volume_total += volume_item
                print(f"  -> Subtotal adicionado: {volume_item:.4f} m³")

        print("\n=======================================")
        print(f"VOLUME TOTAL DO ROMANEIO: {volume_total:.4f} m³")
        print("=======================================")

    except ValueError:
        print("\nErro: Por favor, insira apenas valores numéricos válidos. Use ponto (.) para decimais.")

if __name__ == "__main__":
    calcular_romaneio_lote()