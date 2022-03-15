import request from '@/utils/request';

export const reqConsultRecordList = (page,limit) => request({ url: `/admin/product/baseTrademark/${page}/${limit}`, method: 'get' });
