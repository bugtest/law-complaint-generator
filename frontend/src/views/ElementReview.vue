<template>
  <div class="element-review-container">
    <el-header class="page-header">
      <el-link @click="$router.push(`/case/${caseId}`)">返回案件详情</el-link>
      <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
    </el-header>

    <el-main v-loading="loading">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>原告信息</template>
            <el-form label-width="100px">
              <el-form-item label="姓名">
                <el-input v-model="elements.plaintiff.name" />
              </el-form-item>
              <el-form-item label="身份证号">
                <el-input v-model="elements.plaintiff.id_number" />
              </el-form-item>
              <el-form-item label="地址">
                <el-input v-model="elements.plaintiff.address" type="textarea" />
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="elements.plaintiff.phone" />
              </el-form-item>
            </el-form>
          </el-card>

          <el-card style="margin-top: 20px">
            <template #header>被告信息</template>
            <el-form label-width="100px">
              <el-form-item label="姓名">
                <el-input v-model="elements.defendant.name" />
              </el-form-item>
              <el-form-item label="身份证号">
                <el-input v-model="elements.defendant.id_number" />
              </el-form-item>
              <el-form-item label="地址">
                <el-input v-model="elements.defendant.address" type="textarea" />
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="elements.defendant.phone" />
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>诉讼请求</template>
            <div v-for="(claim, index) in elements.claims" :key="index" style="display: flex; gap: 10px; margin-bottom: 10px">
              <el-input v-model="claim.content" placeholder="请求内容" />
              <el-button type="danger" @click="elements.claims.splice(index, 1)">删除</el-button>
            </div>
            <el-button @click="elements.claims.push({ order: elements.claims.length + 1, content: '' })">添加请求</el-button>
          </el-card>

          <el-card style="margin-top: 20px">
            <template #header>事实与理由</template>
            <el-input v-model="elements.facts_and_reasons" type="textarea" :rows="10" />
          </el-card>

          <el-card style="margin-top: 20px">
            <template #header>证据清单</template>
            <div v-for="(evidence, index) in elements.evidence_list" :key="index" style="display: flex; gap: 10px; margin-bottom: 10px">
              <el-input v-model="evidence.name" placeholder="证据名称" style="width: 100px" />
              <el-input v-model="evidence.purpose" placeholder="证明目的" />
              <el-button type="danger" @click="elements.evidence_list.splice(index, 1)">删除</el-button>
            </div>
            <el-button @click="elements.evidence_list.push({ name: '', purpose: '', page: null })">添加证据</el-button>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const caseId = route.params.id

const loading = ref(false)
const saving = ref(false)

const elements = reactive({
  plaintiff: { name: '', id_number: '', address: '', phone: '' },
  defendant: { name: '', id_number: '', address: '', phone: '' },
  claims: [],
  facts_and_reasons: '',
  evidence_list: []
})

const fetchElements = async () => {
  loading.value = true
  try {
    const response = await api.get(`/api/cases/${caseId}/elements`)
    const data = response.data
    if (data.plaintiff) Object.assign(elements.plaintiff, data.plaintiff)
    if (data.defendant) Object.assign(elements.defendant, data.defendant)
    if (data.claims) elements.claims = data.claims
    if (data.facts_and_reasons) elements.facts_and_reasons = data.facts_and_reasons
    if (data.evidence_list) elements.evidence_list = data.evidence_list
  } catch (error) {
    if (error.response?.status !== 404) {
      ElMessage.error('加载失败')
    }
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    await api.put(`/api/cases/${caseId}/elements`, {
      ...elements,
      reviewed: true
    })
    ElMessage.success('保存成功')
    router.push(`/case/${caseId}`)
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(fetchElements)
</script>

<style scoped>
.element-review-container {
  height: 100vh;
}

.page-header {
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
