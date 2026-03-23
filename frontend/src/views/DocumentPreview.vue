<template>
  <div class="document-preview-container">
    <el-header class="page-header">
      <el-link @click="$router.push(`/case/${caseId}`)">返回案件详情</el-link>
      <el-button type="primary" @click="handleDownload">下载文书</el-button>
    </el-header>

    <el-main>
      <el-card>
        <template #header>
          <span>文书预览</span>
        </template>
        <div class="preview-placeholder">
          <el-icon :size="64"><Document /></el-icon>
          <p>文书已生成，请下载查看</p>
          <el-button type="primary" @click="handleDownload">下载 Word 文档</el-button>
        </div>
      </el-card>
    </el-main>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const caseId = route.params.id

const handleDownload = () => {
  window.open(`/api/cases/${caseId}/documents/latest/download`, '_blank')
}
</script>

<style scoped>
.document-preview-container {
  height: 100vh;
}

.page-header {
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #909399;
}

.preview-placeholder p {
  margin: 20px 0;
}
</style>
