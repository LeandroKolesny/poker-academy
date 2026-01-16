# Design: Layout de Partições para Páginas Admin

**Data:** 2026-01-15
**Status:** Aprovado
**Páginas afetadas:** AdminStudentGraphs, AdminMonthlyDatabase, AdminLeakManagement

---

## Resumo

Reorganizar as páginas de administração (student-graphs, monthly-database, leak-management) para exibir alunos agrupados por partição em um layout de cards colapsáveis, com modal para visualizar/gerenciar dados individuais.

---

## Layout da Página

```
┌──────────────────────────────────────────────────────────────┐
│  [Título da Página]                            [Ano: 2026 ▼] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ▼ PARTIÇÃO GRINDERS (5 alunos)                         │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │  │
│  │  │  👤    │  │  👤    │  │  👤    │  │  👤    │  ...   │  │
│  │  │ João   │  │ Maria  │  │ Pedro  │  │ Ana    │        │  │
│  │  │ [Ver]  │  │ [Ver]  │  │ [Ver]  │  │ [Ver]  │        │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ▶ PARTIÇÃO PRO PLAYERS (3 alunos)           [Colapsado]│  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Comportamento

- Primeira partição expandida por padrão
- Clique no header da partição expande/colapsa
- Cards em grid responsivo (4 colunas desktop, 2 mobile)
- Filtro de ano no header afeta dados do modal

---

## Modal do Aluno

Ao clicar "Ver" no card, abre modal com dados do aluno:

```
┌──────────────────────────────────────────────────────────────┐
│  [Título] - Nome do Aluno                            [X]     │
│  email@aluno.com                                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────┬──────────────┬─────────────┬─────────────────┐   │
│  │ Mês    │ Conteúdo     │ Data Envio  │ Ações           │   │
│  ├────────┼──────────────┼─────────────┼─────────────────┤   │
│  │ Jan    │ [conteúdo]   │ 15/01/2026  │ [Ações]         │   │
│  │ Fev    │ [conteúdo]   │ 10/02/2026  │ [Ações]         │   │
│  │ Mar    │ ─ vazio ─    │ ─           │ [Upload]        │   │
│  │ ...    │              │             │                 │   │
│  └────────┴──────────────┴─────────────┴─────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Variações por Página

| Página | Coluna Conteúdo | Ações |
|--------|-----------------|-------|
| student-graphs | Thumbnail imagem | Upload, Zoom |
| monthly-database | Ícone arquivo + tamanho | Upload, Download |
| leak-management | Thumbnail + melhorias | Upload, Zoom, Editar |

### Características do Modal

- Botão X vermelho no header (padrão do sistema)
- Max-height: 95vh com scroll interno
- Thumbnail clicável para zoom (ImageZoomModal existente)
- Carrega dados ao abrir (não antes)

---

## Estrutura de Componentes

```
src/components/admin/
├── PartitionStudentLayout.js    ← Componente reutilizável
├── StudentModal.js              ← Modal base genérico
├── AdminStudentGraphs.js        ← Usa PartitionStudentLayout
├── AdminMonthlyDatabase.js      ← Usa PartitionStudentLayout
└── AdminLeakManagement.js       ← Usa PartitionStudentLayout
```

### PartitionStudentLayout.js

Props:
- `title`: Título da página
- `renderModal`: Função que recebe (student, year, onClose) e retorna conteúdo do modal

Responsabilidades:
- Buscar partições com alunos via API existente
- Renderizar cards colapsáveis por partição
- Gerenciar estado de expansão/colapso
- Gerenciar abertura/fechamento do modal
- Filtro de ano

### Uso

```jsx
// AdminStudentGraphs.js
<PartitionStudentLayout
  title="Gerenciamento de Gráficos dos Alunos"
  renderModal={(student, year, onClose) => (
    <GraphsModalContent
      student={student}
      year={year}
      onClose={onClose}
    />
  )}
/>
```

---

## Fluxo de Dados

1. Página carrega → `PartitionStudentLayout` busca `/api/admin/students-by-partition`
2. Admin clica em partição → Expande/colapsa (estado local)
3. Admin clica "Ver" em aluno → Abre modal, passa student + year
4. Modal busca dados específicos do aluno (graphs/databases/leaks)
5. Admin faz upload → Atualiza dados no modal
6. Admin fecha modal → Volta para lista

---

## Alterações Necessárias

### Backend
Nenhuma alteração. APIs existentes:
- `GET /api/admin/students-by-partition`
- `GET /api/admin/student/:id/graphs`
- `GET /api/admin/student/:id/databases`
- `GET /api/admin/student/:id/leaks`
- `POST /api/admin/student/:id/graphs/upload`
- `POST /api/admin/student/:id/databases/upload`
- `POST /api/admin/student/:id/leaks/upload`

### Frontend
1. Criar `PartitionStudentLayout.js`
2. Refatorar `AdminStudentGraphs.js` para usar novo layout
3. Refatorar `AdminMonthlyDatabase.js` para usar novo layout
4. Refatorar `AdminLeakManagement.js` para usar novo layout

---

## Estimativa de Arquivos

| Arquivo | Ação |
|---------|------|
| PartitionStudentLayout.js | Criar (~200 linhas) |
| AdminStudentGraphs.js | Refatorar (~150 linhas) |
| AdminMonthlyDatabase.js | Refatorar (~150 linhas) |
| AdminLeakManagement.js | Refatorar (~150 linhas) |
