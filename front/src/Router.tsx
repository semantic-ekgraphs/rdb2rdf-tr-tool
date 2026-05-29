import { Routes, Route } from "react-router";
// LAYOUTES
// import { MainLayout } from "./layout/main/MainLayout";
import { Main_Layout } from "./layout/main/Main_Layout";
// PAGES
import { Home } from "./view/Home";
import { About } from "./view/About";
import { Dashboard } from "./view/dashboard/Dashboard";
import { DatasouceList } from "./view/datasource/DatasourceList.tsx";
import { DatasourceForm } from "./view/datasource/DatasourceForm.tsx";
import { Import } from "./view/import/Import";
import { OrganizationList } from "./view/registration/organization/OrganizationList";
import { OrganizationForm } from "./view/registration/organization/OrganizationForm";
import { UserList } from './view/registration/user/UserList'
import { UserForm } from './view/registration/user/UserForm'
import { DeltaTableList } from "./view/registration/delta-table/DeltaTableList";
import { DeltaTableForm } from "./view/registration/delta-table/DeltaTableForm";

import { Resource } from './view/exploration/Resource'
import { SuggestVocabulary } from './view/suggest-vocabulary/SuggestVocabulary.tsx'
import { TerminologySaved } from "./view/suggest-vocabulary/VocabularySaved.tsx";
// LLM
import { QuestionAnswer } from './view/llm/Question_Answer'
import { AgentsLLM } from './view/llm/Agents.tsx'
import { BootstrapOntologyExtraction } from './view/llm/BootstrapOntologyExtraction.tsx'


export default function Router() {
	return (
		<Routes>
			<Route path='/' element={<Main_Layout />}>
				<Route path={"/"} element={<Home />} />
				<Route path={"/dashboard"} element={<Dashboard />} />
				<Route path={"/datasets"} element={<DatasouceList />} />
				<Route path={"/datasets/:uri"} element={<Resource />} />
				<Route path={"/datasets/:uri/suggest-vocabulary"} element={<SuggestVocabulary />} />
				<Route path={"/datasets/:uri/suggest-vocabulary/:hasVocab"} element={<SuggestVocabulary />} />
				<Route path={"/datasets/form"} element={<DatasourceForm />} />
				<Route path={"/import"} element={<Import />} />
				{/* REGISTRATIONS */}
				<Route path={"/organizations"} element={<OrganizationList />} />
				<Route path={"/organizations/:uri"} element={<Resource />} />
				<Route path={"/organizations/form"} element={<OrganizationForm />} />
				<Route path={"/users"} element={<UserList />} />
				<Route path={"/users/:uri"} element={<Resource />} />
				<Route path={"/users/form"} element={<UserForm />} />
				<Route path={"/delta-tables"} element={<DeltaTableList />} />
				<Route path={"/delta-tables/form"} element={<DeltaTableForm />} />
				<Route path={"/properties"} element={<Resource />} />
				<Route path={"/resource/:uri"} element={<Resource />} />
				<Route path={"/vocabulary/:uri"} element={<TerminologySaved />} />
				{/* LLM */}
				<Route path={"/question-answer"} element={<QuestionAnswer />} />
				<Route path={"/agents-llm"} element={<AgentsLLM />} />
				<Route path={"/bootstrap-ontology-extraction"} element={<BootstrapOntologyExtraction />} />
				<Route path={"/publishing"} element={<BootstrapOntologyExtraction />} />
				<Route path={"/about"} element={<About />} />
				<Route path={"*"} element={<h1>Page Not Found</h1>} />
			</Route>
		</Routes>
	)
}