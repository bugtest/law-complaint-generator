<template>
  <div class="case-list-container">
    <el-header class="page-header">
      <h2>案件列表</h2>
      <div class="header-actions">
        <el-button type="primary" @click="showNewCaseDialog = true">
          <el-icon><Plus /></el-icon>
          新建案件
        </el-button>
        <el-button @click="$router.push('/templates')">模板管理</el-button>
        <el-button @click="handleLogout">退出</el-button>
      </div>
    </el-header>

    <el-main>
      <el-table :data="cases" v-loading="loading" stripe>
        <el-table-column prop="case_name" label="案件名称" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/case/${row.id}`)">查看</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <!-- New Case Dialog -->
    <el-dialog v-model="showNewCaseDialog" title="新建案件" width="400px">
      <el-input v-model="newCaseName" placeholder="请输入案件名称" />
      <template #footer>
        <el-button @click="showNewCaseDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreateCase">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const cases = ref([])
const loading = ref(false)
const showNewCaseDialog = ref(false)
const newCaseName = ref('')

const fetchCases = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/cases')
    cases.value = response.data
  } catch (error) {
    ElMessage.error('加载案件列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreateCase = async () => {
  if (!newCaseName.value.trim()) {
    ElMessage.warning('请输入案件名称')
    return
  }

  try {
    const response = await api.post('/api/cases', { case_name: newCaseName.value })
    ElMessage.success('创建成功')
    showNewCaseDialog.value = false
    newCaseName.value = ''
    router.push(`/case/${response.data.id}`)
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除案件"${row.case_name}"吗？`, '确认删除', { type: 'warning' })
    await api.delete(`/api/cases/${row.id}`)
    ElMessage.success('删除成功')
    fetchCases()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const getStatusType = (status) => {
  const map = { draft: '', processing: 'warning', completed: 'success' }
  return map[status] || ''
}

const getStatusText = (status) => {
  const map = { draft: '草稿', processing: '处理中', completed: '已完成' }
  return map[status] || status
}

const formatDate = (date) => new Date(date).toLocaleString('zh-CN')

onMounted(fetchCases)
</script>

<style scoped>
.case-list-container {
  height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
}

.page-header h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>
