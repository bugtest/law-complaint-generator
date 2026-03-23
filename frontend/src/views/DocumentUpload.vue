<template>
  <div class="upload-container">
    <el-header class="page-header">
      <el-link @click="$router.push(`/case/${caseId}`)">返回案件详情</el-link>
    </el-header>

    <el-main>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>上传证据 PDF</template>
            <el-upload
              drag
              :auto-upload="false"
              :on-change="(file) => handleFileSelect(file, 'evidence_pdf')"
              accept=".pdf"
            >
              <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
              <div class="el-upload__text">拖拽文件到此处或<em>点击上传</em></div>
            </el-upload>
            <el-button
              type="primary"
              :disabled="!selectedFiles.evidence_pdf"
              :loading="uploading"
              @click="handleUpload('evidence_pdf')"
              style="margin-top: 10px; width: 100%"
            >
              上传 PDF
            </el-button>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>上传整理 Word</template>
            <el-upload
              drag
              :auto-upload="false"
              :on-change="(file) => handleFileSelect(file, 'organized_word')"
              accept=".doc,.docx"
            >
              <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
              <div class="el-upload__text">拖拽文件到此处或<em>点击上传</em></div>
            </el-upload>
            <el-button
              type="primary"
              :disabled="!selectedFiles.organized_word"
              :loading="uploading"
              @click="handleUpload('organized_word')"
              style="margin-top: 10px; width: 100%"
            >
              上传 Word
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const caseId = route.params.id

const selectedFiles = ref({})
const uploading = ref(false)

const handleFileSelect = (file, type) => {
  selectedFiles.value[type] = file.raw
}

const handleUpload = async (type) => {
  const file = selectedFiles.value[type]
  if (!file) return

  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)
  formData.append('doc_type', type)

  try {
    await api.post(`/api/cases/${caseId}/documents`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    ElMessage.success('上传成功')
    router.push(`/case/${caseId}`)
  } catch (error) {
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.upload-container {
  height: 100vh;
}

.page-header {
  border-bottom: 1px solid #e4e7ed;
  margin-bottom: 20px;
}
</style>
