import { expect, test } from '@playwright/test'

test('creates an app, chats, and navigates core pages', async ({ page }) => {
  page.on('console', message => {
    if (message.type() === 'error')
      console.log(`browser console error: ${message.text()}`)
  })
  page.on('pageerror', error => {
    console.log(`browser page error: ${error.message}`)
  })

  await page.goto('/')
  await expect(page.getByRole('heading', { name: 'Apps' })).toBeVisible()

  await page.getByRole('link', { name: /New app/ }).click()
  await expect(page.getByRole('heading', { name: 'New app' })).toBeVisible()
  await page.getByLabel('Name').fill(`UI Smoke ${Date.now()}`)
  await page.getByLabel('Mode').selectOption('chatbot')
  await page.getByLabel('Description').fill('created by ui smoke')
  await page.getByLabel('System prompt').fill('Reply briefly.')
  await page.getByRole('button', { name: 'Create' }).click()

  await expect(page).toHaveURL(/\/chat\?app=/)
  await expect(page.getByRole('heading', { name: 'Chat' })).toBeVisible()
  await page.getByPlaceholder('Message').fill('hello from playwright')
  await page.getByRole('button', { name: /Send/ }).click()
  await expect(page.getByText('Mock response: hello from playwright')).toBeVisible()

  await page.getByRole('link', { name: /Workflow/ }).click()
  await expect(page.getByRole('heading', { name: 'Workflow' })).toBeVisible()

  await page.getByRole('link', { name: /Agent/ }).click()
  await expect(page.getByRole('heading', { name: 'Agent', exact: true })).toBeVisible()

  await page.getByRole('link', { name: /Apps/ }).click()
  await expect(page.getByRole('heading', { name: 'Apps' })).toBeVisible()
})
