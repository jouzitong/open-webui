<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import Search from '$lib/components/icons/Search.svelte';
	import { user } from '$lib/stores';

	const i18n = getContext('i18n');

	type ParameterItem = {
		key: string;
		name: string;
		type: string;
		scope: string;
		value: string;
		status: 'Enabled' | 'Disabled' | 'Draft';
		updatedAt: string;
		description: string;
	};

	const parameterItems: ParameterItem[] = [
		{
			key: 'auth.login.max_attempts',
			name: '登录失败阈值',
			type: 'Number',
			scope: 'Global',
			value: '5',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '单个账号在锁定前允许的连续登录失败次数。'
		},
		{
			key: 'auth.session.expire_minutes',
			name: '会话过期时间',
			type: 'Number',
			scope: 'Global',
			value: '120',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '后台管理登录态的默认过期时长，单位为分钟。'
		},
		{
			key: 'model.default_temperature',
			name: '默认采样温度',
			type: 'Float',
			scope: 'Model',
			value: '0.7',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '新建对话或未单独指定时的模型默认温度。'
		},
		{
			key: 'model.max_context_tokens',
			name: '最大上下文长度',
			type: 'Number',
			scope: 'Model',
			value: '32768',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '单次对话允许拼接的最大上下文 token 数。'
		},
		{
			key: 'analytics.retention_days',
			name: '分析数据保留天数',
			type: 'Number',
			scope: 'Global',
			value: '180',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '聚合分析明细保留时长，超期后执行清理。'
		},
		{
			key: 'knowledge.sync.cron',
			name: '知识库同步周期',
			type: 'String',
			scope: 'Workspace',
			value: '0 */6 * * *',
			status: 'Draft',
			updatedAt: '2026-07-05 10:30',
			description: '外部知识源自动同步表达式，当前仅作静态演示。'
		},
		{
			key: 'upload.file.max_size_mb',
			name: '上传文件大小限制',
			type: 'Number',
			scope: 'Global',
			value: '100',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '普通上传入口允许的单文件最大值，单位 MB。'
		},
		{
			key: 'feature.admin.analytics',
			name: '后台分析开关',
			type: 'String',
			scope: 'Admin',
			value: 'true',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '控制后台 Analytics 菜单及页面是否对管理员展示。'
		},
		{
			key: 'feature.workspace.apps',
			name: '工作台应用市场开关',
			type: 'String',
			scope: 'Workspace',
			value: 'false',
			status: 'Disabled',
			updatedAt: '2026-07-05 10:30',
			description: '控制 workspace 中应用市场模块的显隐。'
		},
		{
			key: 'security.password_policy',
			name: '密码策略配置',
			type: 'Json',
			scope: 'Global',
			value: '{"minLength":8,"requireNumber":true,"requireSymbol":false}',
			status: 'Enabled',
			updatedAt: '2026-07-05 10:30',
			description: '统一定义密码复杂度规则，当前仅作静态展示。'
		}
	];

	let loaded = false;
	let query = '';

	$: filteredItems = parameterItems.filter((item) => {
		const keyword = query.trim().toLowerCase();
		const matchesQuery =
			keyword === '' ||
			item.key.toLowerCase().includes(keyword) ||
			item.name.toLowerCase().includes(keyword) ||
			item.description.toLowerCase().includes(keyword) ||
			item.scope.toLowerCase().includes(keyword) ||
			item.type.toLowerCase().includes(keyword);

		return matchesQuery;
	});

	$: enabledCount = parameterItems.filter((item) => item.status === 'Enabled').length;
	$: draftCount = parameterItems.filter((item) => item.status === 'Draft').length;
	$: disabledCount = parameterItems.filter((item) => item.status === 'Disabled').length;

	const getStatusClass = (status: ParameterItem['status']) => {
		if (status === 'Enabled') {
			return 'bg-emerald-50 text-emerald-700 ring-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-300 dark:ring-emerald-500/20';
		}
		if (status === 'Disabled') {
			return 'bg-gray-100 text-gray-700 ring-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:ring-gray-700';
		}
		return 'bg-amber-50 text-amber-700 ring-amber-200 dark:bg-amber-500/10 dark:text-amber-300 dark:ring-amber-500/20';
	};

	onMount(async () => {
		if ($user?.role !== 'admin') {
			await goto('/');
			return;
		}
		loaded = true;
	});
</script>

{#if loaded}
	<div class="w-full h-full px-[16px] pb-6">
		<div class="mx-auto flex w-full max-w-7xl flex-col gap-4 py-3">
			<div
				class="overflow-hidden rounded-2xl border border-gray-200/70 bg-gradient-to-br from-white via-slate-50 to-sky-50 px-5 py-5 shadow-sm dark:border-gray-800 dark:from-gray-900 dark:via-gray-900 dark:to-gray-950"
			>
				<div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
					<div class="space-y-2">
						<div class="text-xs font-medium uppercase tracking-[0.2em] text-sky-600 dark:text-sky-400">
							Admin Console
						</div>
						<div class="text-2xl font-semibold text-gray-900 dark:text-gray-100">
							{$i18n.t('System Parameters')}
						</div>
						<div class="max-w-3xl text-sm text-gray-600 dark:text-gray-400">
							静态演示页，先用于展示参数中心的结构。后续接入 CRUD 接口后，可直接替换为真实数据源和操作按钮。
						</div>
					</div>

					<div class="grid grid-cols-3 gap-2 lg:min-w-[320px]">
						<div class="rounded-xl border border-gray-200 bg-white/80 px-3 py-3 dark:border-gray-800 dark:bg-gray-900/80">
							<div class="text-xs text-gray-500 dark:text-gray-400">Enabled</div>
							<div class="mt-1 text-xl font-semibold text-gray-900 dark:text-gray-100">
								{enabledCount}
							</div>
						</div>
						<div class="rounded-xl border border-gray-200 bg-white/80 px-3 py-3 dark:border-gray-800 dark:bg-gray-900/80">
							<div class="text-xs text-gray-500 dark:text-gray-400">Draft</div>
							<div class="mt-1 text-xl font-semibold text-gray-900 dark:text-gray-100">
								{draftCount}
							</div>
						</div>
						<div class="rounded-xl border border-gray-200 bg-white/80 px-3 py-3 dark:border-gray-800 dark:bg-gray-900/80">
							<div class="text-xs text-gray-500 dark:text-gray-400">Disabled</div>
							<div class="mt-1 text-xl font-semibold text-gray-900 dark:text-gray-100">
								{disabledCount}
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
				<div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
					<div class="relative w-full lg:max-w-md">
						<div class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
							<Search className="size-4" />
						</div>
						<input
							bind:value={query}
							class="w-full rounded-xl border border-gray-200 bg-gray-50 py-2.5 pl-10 pr-3 text-sm text-gray-900 outline-none transition focus:border-sky-500 focus:bg-white dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100 dark:focus:border-sky-400"
							placeholder="搜索参数名称、Key、类型、说明"
						/>
					</div>

					<div class="text-sm text-gray-500 dark:text-gray-400">
						支持类型：`Number`、`Float`、`String`、`Json`
					</div>
				</div>
			</div>

			<div class="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
						<thead class="bg-gray-50 dark:bg-gray-950/60">
							<tr class="text-left text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">
								<th class="px-4 py-3 font-medium">Parameter</th>
								<th class="px-4 py-3 font-medium">Value</th>
								<th class="px-4 py-3 font-medium">Type</th>
								<th class="px-4 py-3 font-medium">Scope</th>
								<th class="px-4 py-3 font-medium">Status</th>
								<th class="px-4 py-3 font-medium">Updated</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
							{#each filteredItems as item}
								<tr class="align-top">
									<td class="px-4 py-4">
										<div class="text-sm font-medium text-gray-900 dark:text-gray-100">
											{item.name}
										</div>
										<div class="mt-1 font-mono text-xs text-sky-700 dark:text-sky-400">
											{item.key}
										</div>
										<div class="mt-2 max-w-xl text-sm text-gray-500 dark:text-gray-400">
											{item.description}
										</div>
									</td>
									<td class="px-4 py-4">
										<div class="inline-flex rounded-lg bg-gray-100 px-2.5 py-1 font-mono text-sm text-gray-800 dark:bg-gray-800 dark:text-gray-200">
											{item.value}
										</div>
									</td>
									<td class="px-4 py-4 text-sm text-gray-600 dark:text-gray-300">{item.type}</td>
									<td class="px-4 py-4 text-sm text-gray-600 dark:text-gray-300">{item.scope}</td>
									<td class="px-4 py-4">
										<span class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset {getStatusClass(item.status)}">
											{item.status}
										</span>
									</td>
									<td class="px-4 py-4 text-sm text-gray-500 dark:text-gray-400">{item.updatedAt}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

				{#if filteredItems.length === 0}
					<div class="px-4 py-12 text-center text-sm text-gray-500 dark:text-gray-400">
						未找到匹配的系统参数。
					</div>
				{/if}
			</div>
		</div>
	</div>
{/if}
