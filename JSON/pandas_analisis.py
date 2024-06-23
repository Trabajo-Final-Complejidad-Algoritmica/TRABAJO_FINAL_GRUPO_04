import pandas as pd                # incluimos la librería pandas
import matplotlib.pyplot as plt    # incluimos la librería matplotlib

archivo = pd.read_csv('crimenes_febrero_2024.csv')  # subimos el archivo csv al dataframe de pandas

cantidad_crimenes = archivo['AREA-NAME'].value_counts()  # Contar la cantidad de crimenes
total_crimes = cantidad_crimenes.sum()                   # Sumar la cantidad de crimenes
plt.figure(figsize=(8, 5))                              #Tamaños de la figura

bars = plt.bar(cantidad_crimenes.index, cantidad_crimenes, color='#263390') # color de barras azul

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}',
             ha='center', va='bottom', rotation=0)

plt.title('Cantidad de crimenes por area')
plt.xlabel('Area')
plt.ylabel('Cantidad de crimenes')
plt.xticks(rotation=45, ha='right') # Rotación los nombres de las areas
plt.tight_layout()

plt.text(0.4, 0.9, f'Total de Crímenes: {total_crimes}', va='center',
         fontsize=14, color='#263390', transform=plt.gca().transAxes)
plt.show()  # Mostrar el gráfico
#plt.savefig('img/grafico.png')