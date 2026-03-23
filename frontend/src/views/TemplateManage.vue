<template>
  <div class="template-manage-container">
    <el-header class="page-header">
      <el-link @click="$router.push('/')">返回案件列表</el-link>
      <el-button type="primary" @click="uploadDialogVisible = true">上传模板</el-button>
    </el-header>

    <el-main>
      <el-table :data="templates" v-loading="loading">
        <el-table-column prop="name" label="模板名称" />
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="is_default" label="默认" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.is_default" type="success">是</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="uploaded_at" label="上传时间" width="180">
          <template #default="{ row }">
            {{ new Date(row.uploaded_at).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleSetDefault(row)" :disabled="row.is_default">设为默认</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <el-dialog v-model="uploadDialogVisible" title="上传模板" width="400px">
      <el-input v-model="templateName" placeholder="模板名称（可选）" style="margin-bottom: 10px" />
      <el-upload
        drag
        :auto-upload="false"
        :on-change="(file) => selectedFile = file.raw"
        accept=".doc,.docx"
      >
        <div class="el-upload__text">选择 Word 模板文件</div>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpload">上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const templates = ref([])
const loading = ref(false)
const uploadDialogVisible = ref(false)
const templateName = ref('')
const selectedFile = ref(null)

const fetchTemplates = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/templates')
    templates.value = response.data
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  if (templateName.value) formData.append('name', templateName.value)

  try {
    await api.post('/api/templates', formData)
    ElMessage.success('上传成功')
    uploadDialogVisible.value = false
    fetchTemplates()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '上传失败')
  }
}

const handleSetDefault = async (row) => {
  try {
    await api.put(`/api/templates/${row.id}/default`)
    ElMessage.success('设置成功')
    fetchTemplates()
  } catch (error) {
    ElMessage.error('设置失败')
  }
}

const handleDelete = async (row) => {
  await api.delete(`/api/templates/${row.id}`)
  ElMessage.success('删除成功')
  fetchTemplates()
}

onMounted(fetchTemplates)
</script>

<style scoped>
.template-manage-container {
  height: 100vh;
}

.page-header {
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
