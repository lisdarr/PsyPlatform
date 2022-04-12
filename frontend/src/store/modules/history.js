const getDefaultState = () => {
  return {
    synmessages: []
  }
}

const state = getDefaultState()

const mutations = {
  SET_MESSAGES: (state, messages) => {
    state.synmessages = messages
  }
}

const actions = {
  async setMessages({ commit }, messages) {
    commit('SET_MESSAGES', messages)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

