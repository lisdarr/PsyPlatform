/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  const valid_map = ['admin', 'editor', 'consult', 'director', 'adminlim', '王咨询师', '古咨询师', '周导', 'cy', 'rc']
  return valid_map.indexOf(str.trim()) >= 0
}
