<template>
  <div class="case-detail-container">
    <el-header class="page-header">
      <div class="breadcrumb">
        <el-link @click="$router.push('/')">案件列表</el-link>
        <span> / </span>
        <span>{{ caseDetail?.case_name }}</span>
      </div>
    </el-header>

    <el-main v-loading="loading">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>已上传文档</span>
                <el-button type="primary" size="small" @click="$router.push(`/case/${caseId}/upload`)">上传</el-button>
              </div>
            </template>
            <el-empty v-if="documents.length === 0" description="暂无文档" />
            <el-table v-else :data="documents">
              <el-table-column prop="original_filename" label="文件名" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="{ row }">
                  {{ row.type === 'evidence_pdf' ? '证据 PDF' : '整理 Word' }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="80">
                <template #default="{ row }">
                  <el-button size="small" type="danger" @click="handleDeleteDoc(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>
              <span>已生成文书</span>
            </template>
            <el-empty v-if="generatedDocs.length === 0" description="暂无生成文书" />
            <el-table v-else :data="generatedDocs">
              <el-table-column prop="original_filename" label="文件名" />
              <el-table-column label="操作" width="120">
                <template #default="{ row }">
                  <el-button size="small" @click="handleDownload(row)">下载</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>

      <el-card style="margin-top: 20px">
        <template #header>
          <span>操作</span>
        </template>
        <el-button type="primary" @click="handleParse">解析文档</el-button>
        <el-button type="success" @click="$router.push(`/case/${caseId}/elements`)">审核要素</el-button>
        <el-button type="warning" @click="handleGenerate">生成起诉状</el-button>
      </el-card>
    </el-main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const caseId = route.params.id

const caseDetail = ref(null)
const documents = ref([])
const generatedDocs = ref([])
const loading = ref(false)

const fetchDetail = async () => {
  loading.value = true
  try {
    const [caseRes, docRes] = await Promise.all([
      api.get(`/api/cases/${caseId}`),
      api.get(`/api/cases/${caseId}/documents`)
    ])
    caseDetail.value = caseRes.data
    documents.value = docRes.data
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleParse = async () => {
  try {
    await api.post(`/api/cases/${caseId}/parse`)
    ElMessage.success('解析完成')
    fetchDetail()
  } catch (error) {
    ElMessage.error('解析失败')
  }
}

const handleGenerate = async () => {
  try {
    const response = await api.post(`/api/cases/${caseId}/generate`)
    ElMessage.success('生成成功')
    generatedDocs.value.push(response.data)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '生成失败')
  }
}

const handleDeleteDoc = async (row) => {
  await api.delete(`/api/cases/${caseId}/documents/${row.id}`)
  ElMessage.success('删除成功')
  fetchDetail()
}

const handleDownload = (row) => {
  window.open(`/api/cases/${caseId}/documents/${row.id}/download`, '_blank')
}

onMounted(fetchDetail)
</script>

<style scoped>
.case-detail-container {
  height: 100vh;
}

.page-header {
  border-bottom: 1px solid #e4e7ed;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
