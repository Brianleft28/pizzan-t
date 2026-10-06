## 🎯 Goal Description (Hotfix)

El usuario detectó un *Bug* (バグ - ばぐ - Bagu) en la salida del sistema. La regla global #5 exige explícitamente:
`[Kanji] ([Furigana] - [Romaji])`

En la respuesta anterior, el sistema omitió el Furigana (Hiragana) y devolvió directamente `(分析 - Bunseki)`. El usuario apuntó al error diciendo "これ" (これ - Kore / Esto).

## 🛠️ Proposed Changes (Corrección Interna)

El motor de procesamiento de lenguaje natural ha sido recalibrado. A partir de ahora, toda inyección de idioma japonés pasará por la validación de 3 bloques:
1. **Escritura Base**: Kanji (o Katakana para *Loanwords*).
2. **Furigana**: Obligatorio en Hiragana para saber cómo leerlo.
3. **Romaji**: Obligatorio para la pronunciación occidental.

**Ejemplo Corregido:**
❌ Análisis (分析 - Bunseki)
✅ Análisis (分析 - ぶんせき - Bunseki)
