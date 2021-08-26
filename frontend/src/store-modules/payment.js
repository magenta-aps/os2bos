/* Copyright (C) 2019 Magenta ApS, http://magenta.dk.
 * Contact: info@magenta.dk.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/. */


import axios from '../components/http/Http.js'
import Vue from 'vue'
import notify from '../components/notifications/Notify.js'

const state = {
    payment_plan: null,
    payments_meta: null,
    payments: null,
    payment: null,
    internal_payment_recipients: null,
    rates: null,
    payments_are_editable_in_the_past: true, // to be updated by fetchPaymentEditablePastFlag but will generally be true

    // Search filters:
    filters: {
        payment_schedule__payment_id: null,
        case__cpr_number: null,
        recipient_id: null,
        payment_method: null,
        interval: null,
        paid_date_or_date_week: null,
        paid_date_or_date_month: null,
        paid_date_or_date_year: null,
        paid_date_or_date__gte: null,
        paid_date_or_date__lte: null,
        paid: null
    }
}

const getters = {
    getPaymentPlan (state) {
        return state.payment_plan
    },
    getPaymentPlanProperty: (state) => (prop) => {
        if (state.payment_plan[prop]) {
            return state.payment_plan[prop]
        } else {
            return null
        }
    },
    getPayment (state) {
        return state.payment
    },
    getPaymentsMeta (state) {
        return state.payments_meta ? state.payments_meta : false
    },
    getPayments (state) {
        return state.payments ? state.payments : false
    },
    getInternalPaymentRecipients (state) {
        return state.internal_payment_recipients ? state.internal_payment_recipients : false
    },
    getRates (state) {
        return state.rates ? state.rates : false
    },
    getPaymentEditablePastFlag (state) {
        return state.payments_are_editable_in_the_past
    }
}

const mutations = {
    setPaymentPlan (state, payment_plan) {
        state.payment_plan = payment_plan
        state.payments = payment_plan.payments
    },
    setPaymentPlanProperty (state, obj) {
        Vue.set(state.payment_plan, obj.prop, obj.val)
    },
    removePaymentPlanProperty (state, prop) {
        delete state.payment_plan[prop]
    },
    clearPaymentPlan (state) {
        state.payment_plan = {
            payment_type: 'RUNNING_PAYMENT',
            payment_frequency: 'MONTHLY',
            payment_cost_type: 'FIXED', // FIXED, GLOBAL_RATE, or PER_UNIT
            payment_amount: 0
        }
    },
    setPayment (state, payment_data) {
        const idx = state.payments.findIndex(p => p.id === payment_data.id)
        if (idx >= 0) {
            Vue.set(state.payments, idx, payment_data)
        }
    },
    setPayments (state, payments) {
        state.payments = payments
    },
    setPaymentInPayments (state, new_payment) {
        for (let p in state.payments) {
            if (state.payments[p].id === new_payment.id) {
                Vue.set(state.payments, p, new_payment) 
                break
            }
        }
    },
    setPaymentsMeta (state, payments_meta) {
        state.payments_meta = payments_meta
    },
    clearPayment (state) {
        state.payment = {
            payment_type: 'RUNNING_PAYMENT',
            payment_frequency: 'MONTHLY',
            payment_cost_type: 'FIXED', // FIXED, GLOBAL_RATE, or PER_UNIT
            payment_amount: 0
        }
    },
    setPaymentEditRowData (state, obj) {
        let payment_idx = state.payments.findIndex(p => {
            return p.id === obj.idx
        })
        Vue.set(state.payments[payment_idx], obj.prop, obj.val)
    },
    setInternalPaymentRecipients (state, internal_payment_recipients) {
        state.internal_payment_recipients = internal_payment_recipients
    },
    setRates (state, rates) {
        state.rates = rates
    },
    setPaymentEditablePastFlag (state, bool) {
        state.payments_are_editable_in_the_past = bool
    }
}

const actions = {
    updatePayment: function({commit, dispatch}, updated_payment) {
        return axios.patch(`/payments/${ updated_payment.id }/`, updated_payment)
        .then(res => {
            notify('Betaling registreret', 'success')
            commit('setPayment', res.data)
        })
        .catch(err => dispatch('parseErrorOutput', err))
    },
    fetchPayments: function({commit}) {
        axios.get(`/payments/?activity__status=GRANTED`)
        .then(res => {
            commit('setPaymentsMeta', res.data)
            commit('setPayments', res.data.results)
        })
        .catch(err => console.log(err))
    },
    fetchMorePayments: function({commit, state}) {
        axios.get(state.payments_meta.next)
        .then(res => {
            let data = res.data
            let results = state.payments
            for (let result of res.data.results) {
                results.push(result)
            }
            data.results = results
            commit('setPaymentsMeta', data)
            commit('setPayments', data.results)
        })
        .catch(err => console.log(err))
    },
    fetchPayment: function({commit}, payment_id) {
        axios.get(`/payments/${ payment_id }/`)
        .then(res => {
            commit('setPayment', res.data)
        })
        .catch(err => console.log(err))
    },
    fetchPaymentPlan: function({commit}, payment_plan_id) {
        axios.get(`/payment_schedules/${ payment_plan_id }/`)
        .then(res => {
            commit('setPaymentPlan', res.data)
            commit('setPayments', res.data.payments)
        })
        .catch(err => console.log(err))
    },
    fetchInternalPaymentRecipients: function({commit}) {
        axios.get(`/internal_payment_recipients/`)
        .then(res => {
            commit('setInternalPaymentRecipients', res.data)
        })
        .catch(err => console.log(err))
    },
    fetchRates: function({commit}) {
        axios.get(`/rates/`)
        .then(res => {
            commit('setRates', res.data)
        })
        .catch(err => console.log(err))
    },
    fetchPaymentEditablePastFlag: function({commit}) {
        axios.get('/editing_past_payments_allowed/')
        .then(res => {
            commit('setPaymentEditablePastFlag', res.data)
        })
        .catch(err => console.log(err))
    }
}

export default {
    state,
    getters,
    mutations,
    actions
}