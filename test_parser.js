// Teste do parser de arquivos - Simulando exatamente o que o código faz

const testFileName = "03.04.25-Cademito-PreFlop-Equity Drop vs RPS Diferencas_Vanilla e PKO.mp4";

console.log("\n" + "=".repeat(80));
console.log("TESTE DO PARSER");
console.log("=".repeat(80));

console.log(`\n📁 Nome original: "${testFileName}"`);

// Remover extensão do arquivo
const fileName = testFileName.replace(/\.[^/.]+$/, "");
console.log(`📝 Sem extensão: "${fileName}"`);

// Suportar ambos os formatos: com espaço " - " ou sem espaço "-"
// Primeiro tenta com espaço, depois sem espaço
let parts = fileName.split(' - ');
console.log(`\n🔀 Split com ' - ': ${parts.length} partes`);
parts.forEach((p, i) => console.log(`   [${i}] "${p}"`));

if (parts.length < 3) {
  parts = fileName.split('-');
  console.log(`\n🔀 Split com '-': ${parts.length} partes`);
  parts.forEach((p, i) => console.log(`   [${i}] "${p}"`));
}

// Categorias reconhecidas
const validCategories = ['preflop', 'posflop', 'mental', 'icm', 'iniciante'];
console.log(`\n📂 Categorias válidas: ${validCategories.join(', ')}`);

// Procurar pela categoria nos parts
let categoryIndex = -1;
let category = null;

console.log(`\n🔍 Procurando categoria nos parts:`);
for (let i = 0; i < parts.length; i++) {
  const normalized = parts[i].trim().toLowerCase();
  console.log(`   [${i}] "${parts[i]}" → normalizado: "${normalized}"`);
  if (validCategories.includes(normalized)) {
    categoryIndex = i;
    category = parts[i].trim();
    console.log(`   ✅ CATEGORIA ENCONTRADA no índice ${i}: "${category}"`);
    break;
  }
}

console.log(`\n🎯 Resultado:`);
console.log(`   categoryIndex: ${categoryIndex}`);
console.log(`   category: "${category}"`);

if (categoryIndex === -1) {
  console.log(`\n❌ ERRO: Categoria não encontrada!`);
} else if (categoryIndex < 2) {
  console.log(`\n❌ ERRO: Categoria em posição inválida! categoryIndex=${categoryIndex}, esperado >= 2`);
} else {
  const dateStr = parts[0].trim();
  const instructor = parts[1].trim();
  const className = parts.slice(categoryIndex + 1).join('-').trim();

  console.log(`\n✅ SUCESSO! Parseado:`);
  console.log(`   Data: "${dateStr}"`);
  console.log(`   Instrutor: "${instructor}"`);
  console.log(`   Categoria: "${category}"`);
  console.log(`   Nome da aula: "${className}"`);
}

console.log("\n" + "=".repeat(80) + "\n");

